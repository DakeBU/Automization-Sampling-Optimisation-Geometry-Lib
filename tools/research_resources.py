"""Pinned bibliographic intake; never awards Lean or source-fidelity credit.

The normal check/build is offline. ``refresh`` fetches the two user-selected
sources and proposes a reviewable metadata diff; it never imports Lean code,
changes a toolchain, schedules a theorem, or executes an upstream program.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'research-wiki/resource-intake.json'
FORUM = 'https://optimization-x-ai.github.io/resources/'
REPO = 'https://github.com/optsuite/optlib'
PIN = '5da27c5f95aa6a8a45b8c14b968ade4c13ff18c3'
ALLOWED = ('ai_assisted_workflow', 'formal_methods', 'education', 'modeling', 'algorithms', 'lower_bounds')


def clean(text: str) -> str:
    return re.sub(r'\s+', ' ', unescape(text)).strip()


class ForumParser(HTMLParser):
    """Read only the six resource sections: title, URL, supplied date, order."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.sections = []
        self.section = None
        self.row = None
        self.capture = None
        self.updated = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'time' and attrs.get('datetime'):
            self.updated = attrs['datetime']
        if tag == 'section' and 'resource-section' in attrs.get('class', '').split():
            self.section = {'id': attrs['aria-labelledby'], 'title': '', 'items': []}
        if self.section is None:
            return
        if tag == 'h2':
            self.capture = 'heading'
        elif tag == 'li':
            self.row = {'title': '', 'url': '', 'tail': ''}
        elif tag == 'a' and self.row is not None:
            self.row['url'] = attrs.get('href', '')
            self.capture = 'title'

    def handle_data(self, data):
        if self.section is None:
            return
        if self.capture == 'heading':
            self.section['title'] += data
        elif self.row is not None:
            self.row['title' if self.capture == 'title' else 'tail'] += data

    def handle_endtag(self, tag):
        if tag in ('h2', 'a'):
            self.capture = None
        if tag == 'li' and self.row is not None:
            row = self.row
            stamp = clean(row.pop('tail')).strip('() ')
            row['title'] = clean(row['title'])
            row['listed_date'] = datetime.strptime(stamp, '%b %d, %Y').date().isoformat() if stamp else None
            row['status'] = 'external-reference'
            row['id'] = 'forum-' + hashlib.sha256(row['url'].encode()).hexdigest()[:16]
            self.section['items'].append(row)
            self.row = None
        if tag == 'section' and self.section is not None:
            self.section['title'] = clean(self.section['title'])
            self.sections.append(self.section)
            self.section = None


def parse_forum(raw: bytes) -> dict:
    parser = ForumParser()
    parser.feed(raw.decode('utf-8'))
    if tuple(s['id'] for s in parser.sections) != ALLOWED:
        raise ValueError('Forum section structure changed: review parser before refresh')
    if not all(s['items'] for s in parser.sections):
        raise ValueError('Empty source category: refusing a silently incomplete import')
    return {'url': FORUM, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw),
            'upstream_updated': parser.updated, 'license': 'not-established',
            'reuse': 'Bibliographic titles, links and listed dates only; no copied prose, layout, code or proofs.',
            'verification': 'Page inventory only; papers and their claimed AI involvement are not independently audited.',
            'sections': parser.sections}


def readme_links(text: str) -> list[dict]:
    """Inventory public mathematical/tool links, not jobs, team or session data."""
    selected = {'Code Explanations', 'Topics', 'Lean Projects', 'Publications', 'References'}
    section = subsection = ''
    rows, seen = [], set()
    for line in text.splitlines():
        if line.startswith('## '):
            section, subsection = line[3:].strip(), ''
        elif line.startswith('### '):
            subsection = line[4:].strip()
            if subsection == 'Topics':
                section = 'Topics'
            elif subsection == 'Sponsor' and section == 'Topics':
                section = ''
        elif line.startswith('#### '):
            subsection = line[5:].strip()
        if section not in selected:
            continue
        links = re.findall(r'\[([^\]]+)\]\((https?://[^)]+)\)', line)
        remaining = re.sub(r'\[[^\]]+\]\([^)]+\)', '', line)
        for url in re.findall(r'https?://[^\s<>]+', remaining):
            url = url.rstrip(').,')
            links.append((url.rsplit('/', 1)[-1] + ' (upstream migration reference)', url))
        if section == 'Publications' and line.startswith('- ') and not links:
            rows.append({'section': section, 'topic': subsection, 'title': clean(line[2:]),
                         'url': f'{REPO}/blob/{PIN}/README.md#publications',
                         'link_note': 'Upstream lists this title without a paper URL; link opens its README citation, not an inferred manuscript.',
                         'status': 'external-reference'})
        for label, url in links:
            if (section, url) in seen:
                continue
            seen.add((section, url))
            # A generic "Paper" link needs its full bibliographic context.
            title = re.sub(r'\[[^\]]+\]\([^)]+\)', '', line).strip(' -*()') if label in ('Paper', '(Paper)') else label.strip('`')
            rows.append({'section': section, 'topic': subsection, 'title': clean(title), 'url': url,
                         'status': 'external-reference'})
    return rows


def get(url: str) -> bytes:
    with urlopen(Request(url, headers={'User-Agent': 'Samplinglib-source-inventory/1.0'}), timeout=40) as response:
        return response.read()


def refresh(tree_file: Path | None = None) -> dict:
    raw = get(FORUM)
    readme = get(f'https://raw.githubusercontent.com/optsuite/optlib/{PIN}/README.md')
    toolchain = get(f'https://raw.githubusercontent.com/optsuite/optlib/{PIN}/lean-toolchain')
    license_bytes = get(f'https://raw.githubusercontent.com/optsuite/optlib/{PIN}/LICENSE')
    tree = json.loads(tree_file.read_text(encoding='utf-8')) if tree_file else json.loads(
        get(f'https://api.github.com/repos/optsuite/optlib/git/trees/{PIN}?recursive=1'))
    if tree.get('sha') not in (PIN, '43e5acffc94932e2060873d07148a0e5bb128e41'):
        raise ValueError('Git tree does not match the pinned Optlib commit')
    if tree.get('truncated'):
        raise ValueError('Incomplete Git tree')
    modules = [{'path': item['path'], 'git_blob': item['sha'],
                'area': item['path'].split('/')[1].removesuffix('.lean'),
                'url': f'{REPO}/blob/{PIN}/{item["path"]}', 'status': 'external-reference'}
               for item in tree['tree'] if item['path'].startswith('Optlib/') and item['path'].endswith('.lean')]
    return {'schema_version': 1, 'retrieved': datetime.now(timezone.utc).date().isoformat(),
            'scope': 'Complete six-section Forum link inventory and pinned Optlib module/README mathematical-resource inventory. Not a theorem audit or full-paper import.',
            'forum': parse_forum(raw), 'optlib': {'repository': REPO, 'commit': PIN,
                'license': 'Apache-2.0', 'license_sha256': hashlib.sha256(license_bytes).hexdigest(),
                'copyright': '2026 Chenyi Li, Zichen Wang, Ziyu Wang, Zaiwen Wen; retained upstream, not transferred to Samplinglib.',
                'readme_sha256': hashlib.sha256(readme).hexdigest(), 'toolchain': toolchain.decode().strip(),
                'integration': 'External reference/port source only; existing ASTIS matches are linked from canonical lessons.',
                'modules': modules, 'readme_resources': readme_links(readme.decode())}}


def load(path: Path = CATALOG) -> dict:
    data = json.loads(path.read_text(encoding='utf-8'))
    validate(data)
    return data


def validate(data: dict) -> None:
    if data.get('schema_version') != 1:
        raise ValueError('Unknown resource intake schema')
    forum, opt = data['forum'], data['optlib']
    if forum['url'] != FORUM or opt['commit'] != PIN:
        raise ValueError('Unexpected source identity or Optlib pin')
    if not re.fullmatch('[a-f0-9]{64}', forum['sha256']):
        raise ValueError('Missing source fingerprint')
    if tuple(s['id'] for s in forum['sections']) != ALLOWED:
        raise ValueError('Incomplete category inventory')
    seen = set()
    for section in forum['sections']:
        for row in section['items']:
            if row['id'] in seen or not row['title']:
                raise ValueError('Duplicate/empty resource')
            seen.add(row['id'])
            if row['listed_date']:
                datetime.strptime(row['listed_date'], '%Y-%m-%d')
    for row in [r for s in forum['sections'] for r in s['items']] + opt['modules'] + opt['readme_resources']:
        if row['status'] != 'external-reference':
            raise ValueError('External inventory cannot receive local Lean credit')
        if urlparse(row['url']).scheme not in ('https', 'http'):
            raise ValueError('Resource must have an HTTP(S) destination')
    for module in opt['modules']:
        if module['url'] != f'{REPO}/blob/{PIN}/{module["path"]}':
            raise ValueError('Module link not immutable')
    if len({m['path'] for m in opt['modules']}) != len(opt['modules']):
        raise ValueError('Duplicate upstream module')
    local = (ROOT / 'lean-toolchain').read_text(encoding='utf-8').strip()
    if local != 'leanprover/lean4:v4.33.0':
        raise ValueError('Samplinglib toolchain must remain Lean 4.33.0')
    upstreams = (ROOT / 'Libraries/FirstOrderOptimization/upstreams.yml').read_text(encoding='utf-8')
    if f'pinned_commit: {opt["commit"]}' not in upstreams:
        raise ValueError('Resource catalog and existing formal-upstream pin drifted')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('check', 'refresh', 'source-check'))
    parser.add_argument('--optlib-tree', type=Path, help='Saved GitHub tree response for the pinned commit, if API rate-limited')
    args = parser.parse_args()
    if args.command == 'refresh':
        data = refresh(args.optlib_tree)
        validate(data)
        CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
        print('Updated reviewable bibliography; inspect diff before publishing.')
    else:
        data = load()
        if args.command == 'source-check':
            current = refresh(args.optlib_tree)
            # Retrieval date is not bibliographic change.
            current['retrieved'] = data['retrieved']
            if current != data:
                raise SystemExit('Upstream content changed; run refresh and review, not automatic promotion.')
    print(json.dumps({'forum_items': sum(len(s['items']) for s in data['forum']['sections']),
                      'forum_categories': len(data['forum']['sections']),
                      'optlib_modules': len(data['optlib']['modules']),
                      'optlib_readme_resources': len(data['optlib']['readme_resources']),
                      'lean_credit': 0}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
