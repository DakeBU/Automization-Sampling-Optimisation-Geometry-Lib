"""Uncapped project history from README; eight-row scroll viewport, not data loss."""
from __future__ import annotations

import re
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

import astis_site

ROOT = Path(__file__).resolve().parents[2]
MARKER = 'data-project-news="true"'


def rows(readme: str) -> list[tuple[str, str]]:
    section = readme.split('## News\n', 1)[1].split('\n## ', 1)[0]
    result = re.findall(r'^- \*\*(\d{4}-\d{2}-\d{2}):\*\* (.+)$', section, re.M)
    if not result or [d for d, _ in result] != sorted((d for d, _ in result), reverse=True):
        raise ValueError('README News must contain dated entries, newest first')
    return result  # Never truncate the source history.


def inline(text: str, repository: str) -> str:
    def link(match):
        label, target = match.groups()
        parsed = urlsplit(target)
        if parsed.scheme and parsed.scheme not in {'http', 'https'}:
            raise ValueError('Unsupported News link scheme')
        if not parsed.scheme:
            target = repository.rstrip('/') + '/blob/main/' + target
        return f'<a href="{escape(target)}">{escape(label)}</a>'
    parts, pos = [], 0
    for match in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', text):
        parts.extend([escape(text[pos:match.start()]), link(match)])
        pos = match.end()
    return ''.join(parts) + escape(text[pos:])


def render(readme: str, repository: str) -> str:
    entries = ''.join(f'<li><time datetime="{date}">{date}</time><span>{inline(text, repository)}</span></li>'
                      for date, text in rows(readme))
    return (f'<section class="project-news" {MARKER} aria-labelledby="project-news-title">'
        '<h2 id="project-news-title">News</h2><p>Recent updates first. Scroll within the list for earlier news.</p>'
        '<ol class="project-news-list" tabindex="0" aria-label="Project news, newest first; scroll for earlier updates">'
        + entries + '</ol></section>')


def enrich_site(output: Path) -> None:
    assets = output / 'assets'
    for name in ('project-news.css', 'project-news.js'):
        (assets / name).write_bytes((ROOT / 'website/static' / name).read_bytes())
    path = output / 'index.html'
    text = path.read_text(encoding='utf-8')
    repository = (astis_site._ACTIVE_GIT or astis_site.git_context()).web_root
    if MARKER not in text:
        text = text.replace('</main>', render((ROOT / 'README.md').read_text(encoding='utf-8'), repository) + '</main>', 1)
        text = text.replace('</head>', '<link rel="stylesheet" href="assets/project-news.css"><script defer src="assets/project-news.js"></script></head>', 1)
        path.write_text(text, encoding='utf-8', newline='\n')


def validate_site(output: Path) -> list[str]:
    text = (output / 'index.html').read_text(encoding='utf-8')
    section = re.search(r'<section class="project-news".*?</section>', text, re.S)
    if section is None:
        return ['Missing project News history']
    expected = [d for d, _ in rows((ROOT / 'README.md').read_text(encoding='utf-8'))]
    actual = re.findall(r'<time datetime="([^"]+)">', section[0])
    return [] if actual == expected else ['Project News history is truncated or stale']
