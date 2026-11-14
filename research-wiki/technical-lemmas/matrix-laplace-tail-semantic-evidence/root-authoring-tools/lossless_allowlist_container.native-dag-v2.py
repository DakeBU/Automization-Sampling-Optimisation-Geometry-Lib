#!/usr/bin/env python3
"""ROOT-later lossless container for an explicit, hash-sealed list of regular leaves.

This mechanical packager is not the final public-payload or commit-graph audit.
It never discovers source files, follows links, invokes Git, or accesses a browser.
"""
import argparse
import bz2
import collections
import gzip
import hashlib
import io
import json
import lzma
import os
from pathlib import Path, PurePosixPath
import re
import stat
import tarfile
import zipfile

DEFAULT_MAX_LEAF_BYTES = 256 * 1024 * 1024
DEFAULT_MAX_TOTAL_BYTES = 512 * 1024 * 1024
# The independently inspected native Expr/Level DAG JSON has structural depth
# 14–16. Retain a finite resource bound while scanning every nested collection.
# All private-collection, member, nesting and byte guards remain unchanged.
MAX_STRUCTURED_DEPTH = 32
MAX_NESTING = 6
MAX_ARCHIVE_MEMBERS = 100000
DENIED_COMPONENTS = {
    '.git', 'chrome-tmp', '__pycache__', '.cache', 'cache', 'cache_data',
    'cachestorage', 'gpucache', 'code cache', 'shadercache', 'graphitedawncache',
    'gpupersistentcache', 'extensions_crx_cache', 'component_crx_cache',
}
DENIED_BASENAMES = {
    'preservation_guard.py', 'independent_preservation_guard.py',
    'private_guard.py', 'full_preservation_guard.py', 'git-index.raw',
    'git-index.raw.gz', 'index.private', 'index.private.json',
}
PRIVATE_COLLECTION_KEYS = {
    'all_tracked', 'protected_tracked', 'all_tracked_worktree_bytes_and_modes',
    'foreign_sau_states', 'foreign_states', 'all_discovery_states',
    'foreign_advance_full_state_digests', 'discovery_complete_state_digests',
    'foreign_state_hashes', 'foreign_state_digests', 'foreign_frontier_hashes',
    'all_frontier_raw_hashes', 'all_raw_frontier_hashes',
    'full_preservation_guard', 'whole_workspace_preservation',
}


class Rejected(ValueError):
    pass


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def regular_member_name(value):
    """Canonical POSIX relative names only; no substring ban on `index`/`private`."""
    if not isinstance(value, str) or not value or '\x00' in value or '\\' in value:
        raise Rejected('Manifest/member path must be a nonempty POSIX relative path')
    if value.startswith('/') or re.match(r'^[A-Za-z]:', value):
        raise Rejected('Absolute/drive paths are forbidden')
    parts = value.split('/')
    if any(p in ('', '.', '..') for p in parts):
        raise Rejected('Empty, dot, and parent path components are forbidden')
    if any(p.casefold() in DENIED_COMPONENTS for p in parts):
        raise Rejected('Known local Git/browser/cache component is forbidden')
    basename = parts[-1].casefold()
    if basename in DENIED_BASENAMES:
        raise Rejected('Known private index/guard leaf is forbidden')
    if re.search(r'^(?:index|protected(?:[-_.][^.]+)*|preservation(?:[-_.][^.]+)*|foreign(?:[-_.][^.]+)*|states?|guard)\.private(?:[._-]|$)', basename):
        raise Rejected('Known private index/preservation snapshot filename is forbidden')
    return str(PurePosixPath(value))


def load_manifest(manifest_path):
    manifest_path = Path(manifest_path)
    if manifest_path.is_symlink():
        raise Rejected('Input manifest itself is a symlink')
    raw = manifest_path.read_bytes()
    try:
        value = json.loads(raw)
    except (ValueError, UnicodeDecodeError) as exc:
        raise Rejected('Manifest must be valid UTF-8 JSON') from exc
    rows = value.get('files') if isinstance(value, dict) else value
    if not isinstance(rows, list) or not rows:
        raise Rejected('Manifest requires a nonempty files list (or top-level rows list)')
    result = []
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            raise Rejected('Each manifest row must be an object')
        path = row.get('path', row.get('source_relative_path'))
        if 'path' in row and 'source_relative_path' in row and row['path'] != row['source_relative_path']:
            raise Rejected('Conflicting path/source_relative_path fields')
        path = regular_member_name(path)
        if path in seen:
            raise Rejected('Duplicate manifest leaf: ' + path)
        seen.add(path)
        size = row.get('bytes')
        digest = row.get('sha256')
        if type(size) is not int or size < 0:
            raise Rejected('bytes must be a nonnegative integer: ' + path)
        if not isinstance(digest, str) or not re.fullmatch(r'[0-9a-fA-F]{64}', digest):
            raise Rejected('sha256 must be a 64-digit hexadecimal digest: ' + path)
        result.append({'path': path, 'bytes': size, 'sha256': digest.lower()})
    return raw, result


def open_leaf_without_links(source_base, name, max_bytes):
    """Open each explicit component relative to an already opened directory FD."""
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)
    directory_flags = flags | getattr(os, 'O_DIRECTORY', 0)
    fds = []
    try:
        base = Path(source_base)
        if base.is_symlink():
            raise Rejected('source_base itself is a symlink')
        fds.append(os.open(base, directory_flags))
        parts = name.split('/')
        for component in parts[:-1]:
            fd = os.open(component, directory_flags, dir_fd=fds[-1])
            if not stat.S_ISDIR(os.fstat(fd).st_mode):
                os.close(fd)
                raise Rejected('Non-directory source component: ' + name)
            fds.append(fd)
        fd = os.open(parts[-1], flags | getattr(os, 'O_NONBLOCK', 0), dir_fd=fds[-1])
        fds.append(fd)
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            raise Rejected('Only regular file leaves are accepted: ' + name)
        if st.st_size > max_bytes:
            raise Rejected('Explicit leaf exceeds max-leaf-bytes: ' + name)
        chunks = []
        total = 0
        while True:
            chunk = os.read(fd, min(1024 * 1024, max_bytes + 1 - total))
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > max_bytes:
                raise Rejected('Growing leaf exceeds byte bound: ' + name)
        return b''.join(chunks)
    except OSError as exc:
        raise Rejected('Cannot safely open explicit regular leaf (including symlink rejection): ' + name) from exc
    finally:
        for fd in reversed(fds):
            os.close(fd)


def full_state(value):
    return isinstance(value, dict) and bool({'advance_id', 'discovery_id'} & value.keys()) and bool({'event', 'state'} & value.keys()) and len(value) >= 8


def guard_json(value, location, depth=0, selected_hash_inventory=False):
    if depth > MAX_STRUCTURED_DEPTH:
        raise Rejected('Structured payload depth bound exceeded: ' + location)
    if isinstance(value, dict):
        sample = list(value.items())[:128]
        values = [v for _, v in sample]
        if len(value) >= 32 and sample and sum(full_state(v) for v in values) >= len(sample) * .7:
            raise Rejected('Full foreign advance/discovery state snapshot: ' + location)
        # Large selected-file manifests remain valid. Known private collection keys
        # and actual Git-index record fields are still rejected below.
        selected_inventory = 'files' in value and ('file_count' in value or 'payload_file_count' in value) and bool({'exclusions', 'selection_scope', 'copy_policy', 'scope'} & value.keys())
        if len(value) >= 1000 and sample and not selected_hash_inventory:
            path_count = sum(isinstance(k, str) and '/' in k for k, _ in sample)
            digest_count = sum(isinstance(v, str) and bool(re.fullmatch(r'[0-9a-f]{40,64}', v)) or isinstance(v, dict) and bool({'sha256', 'index_oid', 'index_blob', 'git_index_blob', 'blob', 'mode'} & v.keys()) for v in values)
            if path_count >= len(sample) * .7 and digest_count >= len(sample) * .7:
                raise Rejected('Complete tracked/guard path map: ' + location)
        for key, item in value.items():
            if not isinstance(key, str):
                continue
            low = key.casefold()
            if low in PRIVATE_COLLECTION_KEYS and isinstance(item, (dict, list)) and item:
                raise Rejected('Known full tracked/foreign preservation collection at key ' + key + ': ' + location)
            if re.search(r'(?:raw|base64).*git.?index|git.?index.*(?:raw|base64|bytes)', low) and isinstance(item, (str, list)) and len(item) >= 512:
                raise Rejected('Raw Git index field at key ' + key + ': ' + location)
            if selected_inventory and key == 'files' and isinstance(item, dict):
                if any(isinstance(v, dict) and bool({'index_oid', 'index_blob', 'git_index_blob', 'stage'} & v.keys()) for v in item.values()):
                    raise Rejected('Git index records disguised as selected files: ' + location)
                # Exempt only the large path/hash inventory heuristic at this
                # exact node; every record still receives recursive screening.
                guard_json(item, location, depth + 1, selected_hash_inventory=True)
                continue
            if isinstance(item, (dict, list)):
                guard_json(item, location, depth + 1)
            elif isinstance(item, str) and len(item) >= 128 and item.lstrip().startswith(('{', '[')):
                try:
                    nested = json.loads(item)
                except ValueError:
                    continue
                guard_json(nested, location + '::<structured-string>', depth + 1)
    elif isinstance(value, list):
        sample = value[:128]
        if len(value) >= 32 and sample and sum(full_state(v) for v in sample) >= len(sample) * .7:
            raise Rejected('Full foreign state/ledger record list: ' + location)
        if len(value) >= 1000 and sample and sum(isinstance(v, dict) and 'path' in v and bool({'index_oid', 'index_mode', 'index_blob', 'git_index_blob', 'stage'} & v.keys()) for v in sample) >= len(sample) * .7:
            raise Rejected('Complete Git index record list: ' + location)
        for item in value:
            if isinstance(item, (dict, list)):
                guard_json(item, location, depth + 1)
            elif isinstance(item, str) and len(item) >= 128 and item.lstrip().startswith(('{', '[')):
                try:
                    nested = json.loads(item)
                except ValueError:
                    continue
                guard_json(nested, location + '::<structured-string>', depth + 1)


def guard_payload(data, location, max_bytes, depth=0):
    if depth > MAX_NESTING or len(data) > max_bytes:
        raise Rejected('Nested payload bound exceeded: ' + location)
    if data.startswith(b'DIRC'):
        raise Rejected('Raw Git index binary: ' + location)
    if data.startswith(b'\x1f\x8b'):
        try:
            decoded = gzip.GzipFile(fileobj=io.BytesIO(data)).read(max_bytes + 1)
        except (OSError, EOFError) as exc:
            raise Rejected('Invalid gzip payload: ' + location) from exc
        guard_payload(decoded, location + '::<gzip>', max_bytes, depth + 1)
        return
    if data.startswith((b'BZh', b'\xfd7zXZ\x00')):
        try:
            is_xz = data.startswith(b'\xfd7zXZ\x00')
            stream = lzma.LZMAFile(io.BytesIO(data)) if is_xz else bz2.BZ2File(io.BytesIO(data))
            with stream:
                decoded = stream.read(max_bytes + 1)
        except (OSError, EOFError, lzma.LZMAError) as exc:
            raise Rejected('Invalid compressed payload: ' + location) from exc
        guard_payload(decoded, location + ('::<xz>' if is_xz else '::<bzip2>'), max_bytes, depth + 1)
        return
    if data.startswith(b'PK\x03\x04'):
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            members = archive.infolist()
            if len(members) > MAX_ARCHIVE_MEMBERS:
                raise Rejected('Archive member bound exceeded: ' + location)
            names = set()
            total = 0
            for member in members:
                name = regular_member_name(member.filename.rstrip('/'))
                if name in names:
                    raise Rejected('Duplicate nested member: ' + location)
                names.add(name)
                if stat.S_ISLNK(member.external_attr >> 16):
                    raise Rejected('Nested ZIP symlink: ' + location)
                if member.is_dir():
                    continue
                total += member.file_size
                if total > max_bytes:
                    raise Rejected('Nested archive decoded-byte bound exceeded: ' + location)
                guard_payload(archive.read(member), location + '!' + name, max_bytes, depth + 1)
        return
    if len(data) > 262 and data[257:262] == b'ustar':
        names = set()
        total = 0
        with tarfile.open(fileobj=io.BytesIO(data), mode='r:*') as archive:
            for index, member in enumerate(archive):
                if index >= MAX_ARCHIVE_MEMBERS:
                    raise Rejected('Archive member bound exceeded: ' + location)
                name = regular_member_name(member.name.rstrip('/'))
                if name in names:
                    raise Rejected('Duplicate nested member: ' + location)
                names.add(name)
                if member.issym() or member.islnk():
                    raise Rejected('Nested tar symlink/hardlink: ' + location)
                if not member.isfile():
                    if member.isdir():
                        continue
                    raise Rejected('Nested special archive member: ' + location)
                total += member.size
                if total > max_bytes:
                    raise Rejected('Nested archive decoded-byte bound exceeded: ' + location)
                guard_payload(archive.extractfile(member).read(), location + '!' + name, max_bytes, depth + 1)
        return
    try:
        guard_json(json.loads(data), location)
    except (ValueError, UnicodeDecodeError) as exc:
        if isinstance(exc, Rejected):
            raise
        lines = data.splitlines()
        state_count = 0
        for index, line in enumerate(lines):
            if not line.lstrip().startswith((b'{', b'[')):
                continue
            try:
                item = json.loads(line)
            except (ValueError, UnicodeDecodeError):
                continue
            # JSONL and raw stdout can have only one or two full-map lines.
            # Screen their actual JSON objects independently of ledger length.
            guard_json(item, location + '::<JSON-line>')
            if index < 128:
                state_count += full_state(item)
        if len(lines) >= 32 and state_count >= min(128, len(lines)) * .7:
            raise Rejected('Copied full ledger snapshot: ' + location)


def verify_archive(path, rows):
    expected = {row['path']: row for row in rows}
    checks = []
    seen = set()
    with tarfile.open(path, mode='r:gz') as archive:
        for member in archive:
            if not member.isfile() or member.name in seen or member.name not in expected:
                raise Rejected('Unexpected/duplicate/nonregular output tar member')
            seen.add(member.name)
            data = archive.extractfile(member).read()
            row = expected[member.name]
            if len(data) != row['bytes'] or sha256(data) != row['sha256']:
                raise Rejected('Output member hash/size mismatch: ' + member.name)
            if member.mtime != 0 or member.uid != 0 or member.gid != 0:
                raise Rejected('Output metadata is not normalized: ' + member.name)
            checks.append({**row, 'output_member_verified': True})
    if seen != set(expected):
        raise Rejected('Output tar member set differs from explicit manifest')
    return checks


def package(source_base, manifest, output_archive, custody_json=None, max_leaf_bytes=DEFAULT_MAX_LEAF_BYTES, max_total_bytes=DEFAULT_MAX_TOTAL_BYTES):
    if type(max_leaf_bytes) is not int or max_leaf_bytes < 1:
        raise Rejected('max_leaf_bytes must be positive')
    manifest_bytes, rows = load_manifest(manifest)
    if type(max_total_bytes) is not int or max_total_bytes < 1 or sum(row['bytes'] for row in rows) > max_total_bytes:
        raise Rejected('Selected total exceeds max-total-bytes')
    output = Path(output_archive).absolute()
    custody = Path(custody_json).absolute() if custody_json else Path(str(output) + '.custody.json')
    if not str(output).endswith('.tar.gz'):
        raise Rejected('Output archive must have the distinct intended .tar.gz pathname')
    if output == custody or output.exists() or output.is_symlink() or custody.exists() or custody.is_symlink():
        raise Rejected('Output/custody must be distinct new paths; overwrite is forbidden')
    if not output.parent.is_dir() or not custody.parent.is_dir():
        raise Rejected('Output/custody parent directory must already exist')
    source = Path(source_base).absolute()
    source_names = {source.joinpath(*row['path'].split('/')) for row in rows}
    if output in source_names or custody in source_names or output == Path(manifest).absolute() or custody == Path(manifest).absolute():
        raise Rejected('Output/custody cannot replace source leaves or the input manifest')
    payloads = []
    for row in rows:
        data = open_leaf_without_links(source, row['path'], max_leaf_bytes)
        if len(data) != row['bytes'] or sha256(data) != row['sha256']:
            raise Rejected('Explicit original leaf hash/size mismatch: ' + row['path'])
        guard_payload(data, row['path'], max_leaf_bytes)
        payloads.append((row, data))
    # No extra member or injected manifest changes the actor-selected leaf set.
    with output.open('xb') as raw_output:
        with gzip.GzipFile(fileobj=raw_output, mode='wb', filename='', mtime=0, compresslevel=9) as gz:
            with tarfile.open(fileobj=gz, mode='w', format=tarfile.PAX_FORMAT) as archive:
                for row, data in payloads:
                    member = tarfile.TarInfo(row['path'])
                    member.size = len(data)
                    member.mode = 0o644
                    member.uid = member.gid = 0
                    member.uname = member.gname = ''
                    member.mtime = 0
                    archive.addfile(member, io.BytesIO(data))
    checks = verify_archive(output, rows)
    archive_bytes = output.read_bytes()
    receipt = {
        'schema': 'ROOT-later-lossless-explicit-allowlist-container-custody-v1',
        'container_attribution': 'ROOT later packaging, or a ROOT-invoked local utility; not the original independent actor creating this container.',
        'truth_boundary': 'Mechanical exact-selected-leaf custody only. No new proof, native/source/runtime result, privacy approval, VERIFIED admission, public commit approval, main integration or Goal completion.',
        'source_base': str(source), 'explicit_manifest': str(Path(manifest).absolute()),
        'explicit_manifest_sha256': sha256(manifest_bytes),
        'archive_file': str(output), 'archive_bytes': len(archive_bytes),
        'archive_sha256': sha256(archive_bytes), 'member_count': len(rows),
        'total_selected_leaf_bytes': sum(row['bytes'] for row in rows),
        'member_order': 'exact input manifest order',
        'mtime_uid_gid_zero': True, 'gzip_filename_empty_and_mtime_zero': True,
        'exact_member_set_and_every_leaf_bytes_sha256_verified_after_pack': True,
        'private_guard_screen_boundary': 'Rejects exact known private/cache paths and actual raw-index/full preservation/state-map shapes, including nested tar/gzip/zip. Explicit allowlist plus leaf hashes remains the selection authority; final payload privacy and commit-graph audit remain required.',
        'files': checks,
    }
    with custody.open('x', encoding='utf-8') as stream:
        json.dump(receipt, stream, indent=2, ensure_ascii=False)
        stream.write('\n')
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-base', required=True)
    parser.add_argument('--manifest', required=True)
    parser.add_argument('--output-archive', required=True)
    parser.add_argument('--custody-json')
    parser.add_argument('--max-leaf-bytes', type=int, default=DEFAULT_MAX_LEAF_BYTES)
    parser.add_argument('--max-total-bytes', type=int, default=DEFAULT_MAX_TOTAL_BYTES)
    args = parser.parse_args()
    try:
        result = package(args.source_base, args.manifest, args.output_archive, args.custody_json, args.max_leaf_bytes, args.max_total_bytes)
    except (Rejected, OSError, tarfile.TarError, zipfile.BadZipFile) as exc:
        parser.exit(2, 'REJECTED: ' + str(exc) + '\n')
    print(json.dumps({'archive_file': result['archive_file'], 'archive_sha256': result['archive_sha256'], 'member_count': result['member_count'], 'original_actor_created_container_claimed': False, 'final_public_payload_or_commit_approval': False}))


if __name__ == '__main__':
    main()
