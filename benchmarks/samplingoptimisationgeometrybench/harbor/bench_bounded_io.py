"""One bounded regular-file reader, shared by collection and verification."""
import os
from pathlib import Path
import stat

MAX_BYTES = 65536
MAX_RECEIPT_BYTES = 1024


class InputRejected(ValueError):
    pass


def read_bounded(path, limit=MAX_BYTES):
    if Path(path).is_symlink():
        raise InputRejected('symlink')
    fd = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0))
    with os.fdopen(fd, 'rb') as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode):
            raise InputRejected('not-regular')
        if before.st_size > limit:
            raise InputRejected('too-large')
        raw = stream.read(limit + 1)
        after = os.fstat(stream.fileno())
    if len(raw) > limit:
        raise InputRejected('too-large')
    fields = ('st_dev', 'st_ino', 'st_size', 'st_mtime_ns', 'st_ctime_ns')
    if any(getattr(before, key) != getattr(after, key) for key in fields):
        raise InputRejected('changed-during-read')
    return raw
