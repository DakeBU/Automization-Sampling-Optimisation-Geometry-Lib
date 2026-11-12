"""A small hierarchical reader over the paired benchmark's canonical cores."""
from __future__ import annotations

from html import escape
import json
from pathlib import Path
import re
import shutil
from textwrap import wrap
from urllib.parse import quote

import astis_site
import source_lineage
import sog_bench as bench
import sog_bench_graph_review as graph_review
import bench_portals

ROOT = Path(__file__).resolve().parents[2]
HUB = 'benchmarks/samplingoptimisationgeometrybench/'
MARKER = 'data-sog-bench="true"'
OWNED_ANSWER_PROBE = 'bench_owned_answer_probe'


_MATH_GLYPHS = {
    'ℝ': r'\mathbb{R}', 'ℕ': r'\mathbb{N}', 'ℤ': r'\mathbb{Z}',
    'ℚ': r'\mathbb{Q}', 'ℂ': r'\mathbb{C}', '∇': r'\nabla ',
    '∂': r'\partial ', '∫': r'\int ', '∞': r'\infty ',
    '≼': r'\preceq ', '≽': r'\succeq ', '≤': r'\le ', '≥': r'\ge ',
    '≠': r'\ne ', '∈': r'\in ', '→': r'\to ', '↦': r'\mapsto ',
    '×': r'\times ', '−': '-', '‖': r'\|', '∘': r'\circ ',
    '#': r'\#', '%': r'\%', '&': r'\&',
}
_SUPERSCRIPTS = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺ᵈⁿ', '0123456789-+dn')
_SUBSCRIPTS = str.maketrans('₀₁₂₃₄₅₆₇₈₉₋₊', '0123456789-+')
_MATH_SENTINEL = re.compile(r'[α-ωΑ-Ωℝℕℤℚℂ∇∂∫∞≼≽≤≥≠∈→↦×−‖⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺ᵈⁿ₀₁₂₃₄₅₆₇₈₉₋₊]|[A-Za-z]_[A-Za-z0-9]+\b|[A-Za-z]\^[A-Za-z0-9{]|<=|>=|!=|->')


def inline_prose(text: str) -> str:
    """Lossless typography projection; never change the audited question data.

    Explicit TeX and literal code are protected first. Only compact mathematical
    tokens with an unambiguous glyph/subscript/exponent are promoted. Ambiguous
    or unbalanced tokens stay literal rather than guessing a mathematical parse.
    The exact original token is retained on each generated span for inspection.
    """
    protected = re.split(r'(\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|\$[^$\n]+\$|`[^`\n]+`)', text)

    def token(match):
        original = match.group(0)
        body = original.rstrip('.,;:!?')
        punctuation = original[len(body):]
        descriptive = re.search(r'-[A-Za-z][A-Za-z.-]+$', body)
        if descriptive and _MATH_SENTINEL.search(body[:descriptive.start()]):
            punctuation = body[descriptive.start():] + punctuation
            body = body[:descriptive.start()]
        # Lean/API names are not mathematical subscript expressions. In
        # particular le_div_iff₀ must never become a doubly-subscripted formula.
        identifier = body.split('(', 1)[0]
        if (re.fullmatch(r'[A-Za-z][A-Za-z0-9_\.α-ωΑ-Ω₀-₉]*', identifier)
                and ('.' in identifier or '_' in identifier and re.match(r'(?:[a-z][a-z0-9]+|[A-Z][a-z][a-z0-9]+)_', identifier))):
            return '<code>' + escape(body) + '</code>' + escape(punctuation)
        simple_relation = re.fullmatch(r'[A-Za-z](?:\([^()]*\))?[=<>][A-Za-z0-9().+\-/]+', body)
        if (not (_MATH_SENTINEL.search(body) or simple_relation) or '\\' in body or '`' in body
                or any(body.count(a) != body.count(b) for a, b in [('(', ')'), ('[', ']'), ('{', '}')])
                or '/' in body and (body.startswith(('http:', 'https:')) or '.html' in body)):
            return escape(original)
        tex = re.sub(r'(?<![\^_])\{([^{}]*)\}', r'\\{\1\\}', body)
        tex = re.sub(r'[⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺ᵈⁿ]+', lambda m: '^{'+m.group(0).translate(_SUPERSCRIPTS)+'}', tex)
        tex = re.sub(r'[₀₁₂₃₄₅₆₇₈₉₋₊]+', lambda m: '_{'+m.group(0).translate(_SUBSCRIPTS)+'}', tex)
        tex = re.sub(r'_([A-Za-z0-9]+)', r'_{\1}', tex)
        for raw, symbol in [('<=', r'\le '), ('>=', r'\ge '), ('!=', r'\ne '), ('->', r'\to ')]:
            tex = tex.replace(raw, symbol)
        tex = ''.join(_MATH_GLYPHS.get(char, char) for char in tex)
        return ('<span class="sog-inline-math" data-math-original="' + escape(body, quote=True)
                + '">\\(' + escape(tex) + '\\)</span>' + escape(punctuation))

    parts = []
    for i, part in enumerate(protected):
        if i % 2:
            parts.append('<code>' + escape(part[1:-1]) + '</code>' if part.startswith('`') else escape(part))
        else:
            cursor = 0
            for match in re.finditer(r'\S+', part):
                parts.append(escape(part[cursor:match.start()]))
                parts.append(token(match))
                cursor = match.end()
            parts.append(escape(part[cursor:]))
    return ''.join(parts)


def prose(text: str, *, paragraph: bool = True) -> str:
    # Render unambiguous exponential tokens in otherwise plain prose. Leave
    # existing math spans untouched; this is presentation, not a gold rewrite.
    spans = re.split(r'(\\\[.*?\\\]|\\\(.*?\\\))', text, flags=re.S)
    text = ''.join(span if i % 2 else re.sub(
        r'(?<![A-Za-z\\])(?:[α-ωΑ-Ω])?e\^\{[^{}]+\}',
        lambda match: r'\(' + match.group(0) + r'\)', span)
        for i, span in enumerate(spans))
    # Stack independent comma-separated display identities, without changing
    # the audited source strings or shrinking their mobile math fonts.
    def stack(match, *, inline=False):
        body = match.group(1)
        if r'\begin{' in body:
            if inline:
                return match.group(0)
            # One common authored alignment: equality of two absolute values
            # followed by an estimate. Put each complete sized expression on
            # its own row without modifying the underlying gold formula.
            prefix = r'\begin{aligned}'
            if body.startswith(prefix):
                first, newline, rest = body[len(prefix):].partition(r'\\')
                lhs, relation, rhs = first.partition('&=')
                if (newline and relation and len(first) >= 80 and '&' not in rhs
                        and all(s.strip().startswith(r'\left|') and s.strip().endswith(r'\right|')
                                and s.count(r'\left') == s.count(r'\right') for s in (lhs, rhs))):
                    return r'\[' + prefix + '&' + lhs + r'\\&=' + rhs + newline + rest + r'\]'
            return match.group(0)
        depth, group_depth, sized_depth, start, parts, relations, plus = 0, 0, 0, 0, [], [], []
        in_norm = False
        for index, char in enumerate(body):
            if char in '{}' and (index == 0 or body[index-1] != '\\'):
                depth += 1 if char == '{' else -1
            if depth == 0 and char in '()[]':
                group_depth += 1 if char in '([' else -1
            if depth == 0 and char == '\\':
                delimiter = re.match(r'\\(left|right)(?![A-Za-z])', body[index:])
                if delimiter:
                    sized_depth += 1 if delimiter.group(1) == 'left' else -1
            if depth == group_depth == 0 and body.startswith(r'\|', index):
                in_norm = not in_norm
            if depth == group_depth == sized_depth == 0 and not in_norm and index >= start:
                separator = re.match(r',\s*\\qquad\b', body[index:]) if char == ',' else None
                if separator:
                    parts.append(body[start:index+1])
                    start = index + separator.end()
                elif char == '\n' and re.match(r'\n[ \t]+[+-]', body[index:]):
                    prefix = body[start:index].rstrip()
                    if (prefix and not re.search(r'(?:[=+\-&^_,<>]|\\(?:leq?|geq?|sim|to|approx|cdot|times|pm|mp))$', prefix)
                            and not re.search(r'(?<!\\)\|', body)):
                        # Preserve an authored top-level signed continuation.
                        parts.append(body[start:index])
                        start = index + 1
            if depth == group_depth == 0:
                relation = re.match(r'\\(?:leq?|geq?)(?![A-Za-z])|=', body[index:])
                if relation:
                    relations.append((index, relation.group()))
                if char == '+' and not in_norm and (index == 0 or body[index-1] not in '^_\\'):
                    plus.append(index)
        if inline:
            # Keep long inline monotone chains readable at normal size. The
            # authored comparison terms are unchanged; only their rows move.
            if (len(body.strip()) >= 64 and len(relations) >= 2
                    and not (parts or depth or group_depth or sized_depth or in_norm)
                    and relations[0][1] != '='
                    and all(op[:3] == relations[0][1][:3] for _, op in relations)
                    and not any(token in body for token in (':=', '&', r'\quad', r'\left', r'\right', r'\\',
                                                              r'\lvert', r'\rvert', r'\lVert', r'\rVert'))):
                bounds = [0, *(pos for pos, _ in relations), len(body)]
                rows = [body[i:j].strip() for i, j in zip(bounds, bounds[1:])]
                if all(row and row.count('|') % 2 == 0 for row in rows):
                    return r'\[\begin{aligned}&' + r'\\&'.join(rows) + r'\end{aligned}\]'
            return match.group(0)
        if not parts:
            # A long equality followed by monotone comparisons can wrap at
            # the top-level relations, but sizing pairs stay on one line.
            if (len(body.strip()) > 100 and len(relations) >= 2
                    and relations[0][1] == '=' and relations[1][1] != '='
                    and all(op[:3] == relations[1][1][:3] for _, op in relations[1:])
                    and not any(token in body for token in (':=', '&', r'\quad', r'\\'))
                    and not re.search(r'(?<!\\)\|', body)):
                bounds = [0, *(pos for pos, _ in relations), len(body)]
                rows = [body[i:j].strip() for i, j in zip(bounds, bounds[1:])]
                pairs = ((r'\left', r'\right'), (r'\langle', r'\rangle'),
                         (r'\lvert', r'\rvert'), (r'\lVert', r'\rVert'))
                if all(row and row.count(r'\|') % 2 == 0
                       and all(row.count(left) == row.count(right) for left, right in pairs)
                       for row in rows):
                    return r'\[\begin{aligned}&' + r'\\&'.join(rows) + r'\end{aligned}\]'
            # A long "A ≤ B = C" derivation can put the simplification
            # on its own row at normal font size. Keep other display math
            # intact (in particular, do not split assignments or tuples).
            if (len(body.strip()) > 100 and len(relations) == 2
                    and relations[0][1] != '=' and relations[1][1] == '='
                    and not any(token in body for token in (':=', r'\quad', r'\left', r'\right'))):
                i, j = (pos for pos, _ in relations)
                return (r'\[\begin{aligned}' + body[:i] + '&' + body[i:j]
                        + r'\\&' + body[j:] + r'\end{aligned}\]')
            # Reflow the long sphere norm and the visible sum without editing
            # frozen proof prose or breaking inside grouped delimiters.
            if (len(body.strip()) >= 50 and len(relations) <= 1 and not in_norm
                    and not any(token in body for token in (':=', '&', r'\quad', r'\left', r'\right', r'\\',
                                    r'\langle', r'\rangle', r'\lvert', r'\rvert', r'\lVert', r'\rVert'))
                    and not re.search(r'(?<!\\)\|', body)):
                breaks = []
                if relations:
                    pos, op = relations[0]
                    # Also allow a short left-hand symbol followed by a long
                    # sum/product/integral, e.g. conditional chi-square.
                    if body.lstrip().startswith(r'\|') or (
                            op == '=' and pos <= 24 and
                            re.match(r'\s*\\(?:sum|prod|int)(?![A-Za-z])', body[pos+1:])):
                        breaks.append(pos)
                if len(plus) == 1 and plus[0] > (relations[0][0] if relations else 0):
                    breaks.append(plus[0])
                if breaks:
                    bounds = [0, *breaks, len(body)]
                    rows = [body[i:j].strip() for i, j in zip(bounds, bounds[1:])]
                    if all(row and row.count(r'\|') % 2 == 0 for row in rows):
                        return r'\[\begin{aligned}&' + r'\\&'.join(rows) + r'\end{aligned}\]'
            return match.group(0)
        if not body[start:].strip():
            return match.group(0)
        parts.append(body[start:])
        return r'\[\begin{gathered}' + r'\\'.join(parts) + r'\end{gathered}\]'
    rendered = re.sub(r'\\\[(.*?)\\\]', stack, text, flags=re.S)
    if paragraph:
        def reflow_inline(match):
            if match.group(1) is None:
                return match.group(0)
            equation = stack(match, inline=True)
            closing = r'\end{aligned}\]'
            if match.group(2) and equation.endswith(closing):
                # Keep a trailing sentence mark on the last equation row.
                return equation.removesuffix(closing) + match.group(2) + closing
            return equation

        rendered = re.sub(r'\\\[[\s\S]*?\\\]|\$\$[\s\S]*?\$\$|\$[^$\n]+?\$|\x60[^\x60\n]+\x60|\\\(([\s\S]*?)\\\)([.,;:]?)',
                          reflow_inline, rendered)
    content = inline_prose(rendered)
    return '<p>' + content + '</p>' if paragraph else content


def fold(title: str, content: str) -> str:
    return '<details class="sog-fold"><summary>' + escape(title) + '</summary>' + content + '</details>'


def exercise_pages(exercise: dict) -> str:
    def pages(key: str) -> str:
        start = str(exercise[key])
        return 'pp. ' + start + '–' + str(exercise[key + '_end']) if key + '_end' in exercise else 'p.' + start
    return 'printed ' + pages('book_page') + ' / PDF ' + pages('pdf_page')


def focused_declaration_graph_href(declaration: str) -> str:
    """Open the readable, filtered Lean slice instead of the full overview."""
    from urllib.parse import quote
    return ('../../underlying-lean-graph/index.html?focus=' + quote('decl:' + declaration, safe='')
            + '&amp;view=lean&amp;q=' + quote(declaration, safe=''))


def exercise_panel(core: dict, checked: bool) -> str:
    exercise = core.get('textbook_exercise')
    if not exercise:
        return ''
    source = exercise['book']
    component_mode = bool(exercise.get('source_components'))
    answers = exercise['answer_declarations']
    shared_answer = not component_mode and len(answers) == 1 and len(exercise['parts']) > 1

    def answer_link(declaration: str) -> str:
        label = declaration.rsplit('.', 1)[-1] if component_mode else declaration
        return ('<a href="' + focused_declaration_graph_href(declaration) + '" title="' + escape(declaration)
                + '"><code>' + escape(label) + '</code></a>')

    parts = {}
    for part in exercise['parts']:
        links = ' · '.join(answer_link(d['declaration']) for d in answers if part['id'] in d['supports'])
        parts[part['id']] = '<li>' + escape(part['label']) + ('' if shared_answer else '<br>' + links) + '</li>'
    build = ('Current trusted build records the named owned answer modules and transitive axiom checks.'
             if checked else 'No current aggregate owned-answer build receipt is recorded in this build.')
    pdf = source['pdf_url'] + '#page='
    source_links = '<a href="' + escape(pdf + str(exercise['pdf_page'])) + '">Original source page</a>'
    if 'pdf_page_end' in exercise:
        source_links += (' · <a href="' + escape(pdf + str(exercise['pdf_page_end']))
                         + '">Last source page</a>')
    if component_mode:
        from sog_bench_exercises import question_component

        scope_label = 'Represented source parts and exact Lean scope'
        source_blocks = '<h3>Separate mathematical results and their assumptions</h3>'
        current = question_component(exercise, core['declaration'])
        components = sorted(exercise['source_components'], key=lambda row: row['item_id'] != current)
        for component in components:
            source_blocks += fold(component['title'],
                ('<p class="sog-caption">Source component for this question</p>' if component['item_id'] == current else '')
                + prose(component['statement'])
                + ''.join(prose(r'\[' + formula['tex'] + r'\]') for formula in component['formulae'])
                + ''.join(prose(s) for s in component['assumptions'])
                + '<p><a href="' + escape(component['source']['url']) + '">Component source</a></p>'
                + '<h4>Owned answers for this part</h4><ol>'
                + ''.join(parts[i] for i in component['part_ids']) + '</ol>')
    else:
        scope_label = 'Original exercise, all requested parts and exact Lean scope'
        combined_answer = ('<p>One owned Lean answer covers the listed parts: '
                           + answer_link(answers[0]['declaration']) + '.</p>') if shared_answer else ''
        source_blocks = ('<h3>Original exercise · faithful ASTIS restatement</h3>'
            + prose(exercise['source_statement'])
            + ''.join(prose(s) for s in exercise['source_assumptions'])
            + '<h3>Requested parts and owned answers</h3>' + combined_answer
            + '<ol>' + ''.join(parts.values()) + '</ol>')
    if component_mode:
        boundary = 'These Lean results cover only the named components; compilation and QA admission are separate.'
    elif bench.has_lean(core):
        boundary = ('The owned answer is a library reference, not a submission. The separate fixed Lean task '
                    'covers the mathematical conclusion only, not the full explanatory proof or textbook.')
    else:
        boundary = ('The displayed Lean is an owned answer, not an equivalent Lean challenge '
                    'or full textbook certification.')
    heading = prose('Numbered textbook exercise · ' + source['title'] + ' · Exercise ' + exercise['number'])
    details = fold(scope_label,
            prose(', '.join(source['authors']) + ' · ' + source['edition'] +
                  ' · ' + exercise_pages(exercise))
            + '<p>' + source_links + ' · '
            '<a href="textbook-exercises/index.html">Numbered exercise directory</a></p>'
            + prose(exercise['wording_status'])
            + source_blocks
            + ''.join(prose(s) for s in exercise['context_notes'])
            + '<h3>Remaining formal boundary</h3>' + ''.join(prose(s) for s in exercise['unformalized_context'])
            + prose(build + ' ' + boundary)
            + prose(source['rights_boundary']))
    return heading + ('<div class="sog-exercise-scope">' + details + '</div>'
                      if component_mode else details)


def exercise_index(cores: list[dict], checked: bool) -> str:
    import sog_bench_exercises
    rows = sog_bench_exercises.projection(cores, bench.editorial_review(cores)['items'], checked)
    cards = []
    for row in rows:
        labels = {component['item_id']: component['title'] for component in row.get('source_components', [])}
        questions = ''.join('<li><a href="../' + q['core_id'] + '.html">'
                           + escape(labels.get(q.get('component_id'), q['core_id'])) + '</a> · '
                           + escape(q['editorial']) + '</li>' for q in row['questions'])
        editorial = (prose(str(len(row['represented_components_with_accepted_qa'])) + ' of ' + str(len(labels))
                     + ' represented source components have an accepted question.') if labels else '')
        cards.append('<section><h2>' + escape(row['book']['title']) + ' · Exercise '
                     + escape(row['number']) + '</h2>' + prose(row['book']['edition'] +
                       ' · ' + exercise_pages(row)) + '<ul>' + questions + '</ul>' + editorial
                     + prose('Named owned answer declarations: ' + str(len(row['answer_declarations']))
                             + '. Current trusted module build recorded: ' + str(checked).lower() + '.')
                     + ''.join(prose(s) for s in row['unformalized_context']) + '</section>')
    return (f'<article class="sog-reader" {MARKER}><p><a href="../index.html">Bench</a></p><h1>Numbered textbook exercises</h1>'
            '<p>Actual source-numbered questions, original mathematical answers and existing owned Lean/graph mappings. Editorial admission, compiled core answers and a fixed Lean reconstruction challenge are separate states. This directory is not whole-book exercise coverage.</p>'
            + ''.join(cards) + '<p><a href="../downloads/textbook-exercise-map.json">Exact source/part/answer metadata</a> · '
            '<a href="../downloads/TEXTBOOK_EXERCISES.md">Intake and contribution rules</a></p></article>')


def domain_names(core: dict) -> str:
    labels = bench.curriculum.curriculum()['domains']
    return ' / '.join(labels[d] for d in core['library_domains'])


def review_panel(core: dict, row: dict | None = None) -> str:
    row = row if row is not None else bench.editorial_review([core])['items'][core['id']]
    label = {'accepted': 'AI editorial review accepted', 'accepted-after-repair': 'AI editorial review accepted after a separately reviewed correction',
             'pending': 'Independent QA review pending', 'stale': 'Previous review is stale for this content',
             'repair-required': 'Editorial repair required', 'reject': 'Editorial review rejected'}[row['editorial']]
    detail = prose(label + '. This is not canonical theorem publication, full Lean coverage or empirical difficulty calibration.')
    if row.get('remaining_unformalized'):
        detail += '<ul>' + ''.join('<li>' + escape(s) + '</li>' for s in row['remaining_unformalized']) + '</ul>'
    if row.get('issues'):
        detail += '<ul>' + ''.join('<li>' + escape(str(s)) + '</li>' for s in row['issues']) + '</ul>'
    detail += '<p><a href="downloads/editorial-review.json">Content-bound review status and evidence hashes</a> · <a href="https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/tree/main/benchmarks/samplingoptimisationgeometrybench/reviews">Independent reports and frozen inputs</a>. Historical rejected wording is audit material, not training gold.</p>'
    return fold('Editorial review and exact formal-coverage boundary', detail)


def home(cores: list[dict]) -> str:
    return bench_portals.home(cores, bench.curriculum.graph_items())


def local_navigation(tail: str) -> str:
    prefix = '../' * tail.count('/')
    links = [('index.html', 'Overview'), ('curriculum/index.html', 'Browse tasks'),
             ('training/index.html', 'Train'), ('evaluation/index.html', 'Evaluate'),
             ('experts/index.html', 'Expert review')]
    return '<nav class="sog-local-nav" aria-label="Bench workflow"><a href="'+prefix+'index.html">Bench overview</a><details class="sog-tools"><summary>Tools</summary>' + ''.join(
        '<a href="' + prefix + path + '"' + (' aria-current="page"' if tail == path else '') + '>' + label + '</a>'
        for path, label in links) + '</details></nav>'


def training_page() -> str:
    return bench_portals.training_page()


def training_guide() -> str:
    return (f'<article class="sog-reader" {MARKER}><h1>Training data and task API</h1>'
        '<p>Use the reviewed public curriculum for training or development. Do not call it an unseen test. <a href="../downloads/ECOSYSTEM.md">Full ecosystem and environment contract</a>.</p>'
        '<section><h2>1. Choose what your agent can see</h2><div class="sog-grid">'
        '<article><h3>Agent task packages</h3><p>One instruction, exact prompt, environment contract and response template per task. No reference answers or expert source anchors in this ZIP.</p><a class="button primary" href="../downloads/agent-tasks.zip" download>Download prompt-only tasks</a></article>'
        '<article><h3>Reviewed training pairs</h3><p>Original reference formula proofs or aligned Lean references, in messages-format JSONL. These contain answers; keep them away from evaluation prompts.</p><a class="button" href="../downloads/training-pairs.jsonl" download>Download training pairs</a></article></div></section>'
        '<section><h2>2. Keep identities and environments fixed</h2><p>Read <a href="../downloads/task-index.json">task-index.json</a>. Select by track, domain or level, then fetch the linked prompt.json and task.json. Each keeps the original family, public-dev split and content binding; the environment records Lean 4.33.0, Mathlib manifest and evaluator source hashes.</p>'
        + astis_site.code_html('python tools/sog_bench.py check\npython tools/sog_bench.py export --output .astis/my-bench-export')
        + '<p>Instructions and environment/verifier contracts are separate. No Terminal-Bench task content is imported; this site is not a hosted agent runner.</p></section>'
        '<section><h2>3. Run graph tasks in Harbor</h2><p>Optional native tasks use a separate JSON verifier, a digest-pinned Python image and Harbor 0.25.0. The CI runs oracle and empty-answer software fixtures, not models. This does not execute submitted Lean.</p>'
        '<p><a class="button" href="../downloads/harbor-graph-tasks.zip" download>Download Harbor operator package</a> <a href="../downloads/HARBOR.md">Runtime requirements, commands and limitations</a></p>'
        '<p class="sog-caption">Includes oracle answers and verifier material: never give this full ZIP to an agent as closed-book context. Use the prompt-only download above for model inputs. Native runtime acceptance is recorded separately in the CI evidence.</p></section>'
        '<section><h2>4. Prevent train/test leakage</h2><p>Paired views and derived variants stay in the same family. All current families are public-dev. Publishing a solution makes it unsuitable as a new unseen test; changing a split label cannot undo exposure.</p><p><a href="../evaluation/index.html">Record an evaluation run</a> · <a href="../downloads/LICENSE_SCOPE.md">Rights and restricted-source boundaries</a> · <a href="../downloads/manifest.json">Exact export hashes</a></p></section></article>')


def experts_page(cores: list[dict], graph_ids: set[str], known: dict) -> str:
    from urllib.parse import quote
    def graph_link(decl):
        kind, node = bench.graph_anchor(decl.full_name, decl.source_file, graph_ids)
        if node is None:
            return 'Graph not indexed'
        label = 'Declaration in Lean Graph' if kind == 'declaration' else 'Owning module in Lean Graph'
        return '<a href="../../../underlying-lean-graph/index.html?focus=' + quote(node, safe='') + '">' + label + '</a>'
    sections = []
    for domain, label in bench.curriculum.curriculum()['domains'].items():
        rows = []
        for c in cores:
            if domain != c['library_domains'][0]:
                continue
            decl = known[c['declaration']]
            href, _ = astis_site.source_href(decl, from_path=HUB + 'experts/index.html')
            additional = []
            related = c.get('supporting_declarations', []) + c.get('textbook_exercise', {}).get('answer_declarations', [])
            for result in {r['declaration']: r for r in related}.values():
                target = known[result['declaration']]
                result_href, _ = astis_site.source_href(target, from_path=HUB + 'experts/index.html')
                additional.append('<li><code>' + escape(target.short_name) + '</code> · ' + graph_link(target)
                    + ' · <a href="' + escape(result_href) + '">Source</a></li>')
            rows.append('<li id="' + c['id'] + '"><a href="../' + c['id'] + '.html">' + escape(c['title']) + '</a>'
                '<p><code>' + escape(decl.short_name) + '</code> · ' + graph_link(decl) + ' · '
                '<a href="' + escape(href) + '">Exact source</a></p>'
                '<p class="sog-caption">' + ('Aligned Lean task; explanatory scope is separate.' if bench.has_lean(c)
                                              else 'Formal support, not an aligned fixed Lean task.') + '</p>'
                + (fold('Additional owned results and answer parts', '<ul>' + ''.join(additional) + '</ul>') if additional else '') + '</li>')
        sections.append(fold(label + ' · ' + str(len(rows)) + ' task cores', '<ul class="sog-expert-list">' + ''.join(rows) + '</ul>'))
    return (f'<article class="sog-reader" {MARKER}><h1>Expert review</h1>'
        '<p>Start from a task, inspect its mathematical proof, then locate the real library result. Each core is listed once under its first library; all additional domain memberships remain visible in its task and curriculum.</p>'
        '<p><a href="../downloads/expert-graph-positions.json">Machine-readable graph anchors and coverage boundaries</a> · <a href="../graph-json/index.html">Audited structural graph tasks</a></p>'
        '<p class="sog-caption">An anchor is a location, not a proof edge. Imports, compiled proof-body occurrences and conceptual parallels have different meanings. Existing Lean support does not certify an entire natural-language answer.</p>'
        + ''.join(sections) + '</article>')


def track_page(cores: list[dict], track: str) -> str:
    title = 'Natural-language QA' if track == 'natural-language' else 'Lean-assisted QA'
    cores = [c for c in cores if track in c['track_levels']]
    cards = ''.join('<article><small>' + escape(domain_names(c)) + ' · ' + escape(c['track_levels'][track]) + ' (provisional)</small><h2>'
        + escape(c['title']) + '</h2><p>' + escape(c['id']) + ' · 4 rubric points · public-dev</p>'
        '<a class="button" href="../' + c['id'] + '.html?track=' + track + '#' + track + '">Open question</a></article>' for c in cores)
    return (f'<article class="sog-reader" {MARKER}><p><a href="../index.html">Bench overview</a></p><h1>{title}</h1>'
        f'<p>{len(cores)} available views. Missing equivalent Lean tasks remain gaps, not borrowed proof credit. Reference answers stay closed until you choose to read them.</p>'
        '<div class="sog-grid">' + cards + '</div></article>')


def prompt_actions(core: dict, track: str, review: dict) -> str:
    if review['editorial'] not in ('accepted', 'accepted-after-repair'):
        return ''
    path = 'downloads/tasks/' + core['id'] + '/' + track + '/prompt.json'
    return ('<p class="sog-prompt-actions"><button type="button" data-sog-copy-prompt="' + path
            + '">Copy model prompt (JSON)</button> <a download href="' + path + '">Download prompt-only task</a>'
            '<span data-sog-copy-status role="status" aria-live="polite"></span></p>')


def core_page(core: dict, checked: bool, graph_ids: set[str] | None = None, known: dict | None = None, structural: list[dict] | None = None, review_row: dict | None = None) -> str:
    from urllib.parse import quote
    review_row = review_row or bench.editorial_review([core])['items'][core['id']]
    rel = HUB + core['id'] + '.html'
    known = known or astis_site._SOURCE_BY_NAME or {d.full_name: d for d in astis_site.scan_project_sources()[1]}
    declaration = known[core['declaration']]
    href, _ = astis_site.source_href(declaration, from_path=rel)
    anchor_kind, graph_id = bench.graph_anchor(core['declaration'], core['source_file'], graph_ids)
    anchor_label = {'declaration': 'Declaration anchor', 'owning-module': 'Owning-module anchor',
                    'not-indexed': 'Not indexed in Lean Graph', 'not-checked': 'Graph position not checked'}[anchor_kind]
    owned_original = bench.ORIGINAL_EXAMPLE_ANSWERS.get(core['source_file']) == core['declaration']
    graph_label = ('Locate the existing Lean declaration' if anchor_kind == 'declaration'
                   else 'Locate the owning module (declaration not yet indexed in this graph)')
    graph_href = ('../../underlying-lean-graph/index.html?focus=' + quote(graph_id, safe='')
                  if graph_id is not None else None)
    if anchor_kind == 'declaration':
        graph_href = focused_declaration_graph_href(core['declaration'])
    graph_short = f'<a href="{graph_href}">Lean Graph ↗</a> · ' if graph_href else ''
    graph_detail = f' · <a href="{graph_href}">{graph_label}</a>' if graph_href else ' · ' + anchor_label
    status = 'Trusted reference compilation recorded for this source state.' if checked else 'No current trusted-reference compiler receipt recorded in this build.'
    assumptions = '<ul>' + ''.join('<li>' + prose(s, paragraph=False) + '</li>'
                                   for s in core['assumptions']) + '</ul>'
    proof = '<ol>' + ''.join('<li>' + prose(s) + '</li>' for s in core['steps']) + '</ol>'
    rubric = '<ol>' + ''.join('<li>' + inline_prose(r['criterion']) + ' (1 point)</li>' for r in core['rubric']) + '</ol>'
    support_title = ('Owned Lean answer and proof-step correspondence' if core.get('textbook_exercise')
                     else 'Formal support and missing Lean alignment')
    lean = (prose(core['lean_explanation']) + '<div data-lean-code-panel><button type="button" data-lean-copy>Copy Lean reference</button><span data-lean-copy-status role="status" aria-live="polite"></span>'
            + astis_site.code_html(core['lean_reference']) + '</div>'
            '<p><a href="downloads/lean/' + core['id'] + '-reference.lean" download>Download runnable reference</a></p>')
    if not bench.has_lean(core):
        lean = prose(core['lean_explanation'])
        if core.get('support_source_view'):
            lean += (fold('Supporting library Lean (not an aligned QA task)',
                '<div data-lean-code-panel><button type="button" data-lean-copy>Copy supporting module</button>'
                '<span data-lean-copy-status role="status" aria-live="polite"></span>'
                + astis_site.code_html(core['support_lean_source']) + '</div>'
                '<p><a href="downloads/lean/' + core['id'] + '-support.lean" download>Download exact supporting module</a>'
                ' · Uses the project toolchain and its listed imports; not a standalone replacement QA proof.</p>'))
    formal_view = ('<section id="lean"><h2>Lean question</h2><p>Keep the target and context fixed; replace the comment slot with your proof. Ancestor libraries are allowed, but the target module is not imported directly.</p>'
        + prompt_actions(core, 'lean', review_row)
        + fold('Show fixed Lean task', astis_site.code_html(core['lean_task'])
               + '<p><a href="downloads/lean/' + core['id'] + '-task.lean.txt" download>Download task template</a></p>')
        + fold('Reference Lean and explanation', lean) + prose(status) + '</section>') if bench.has_lean(core) else (
        '<section id="lean"><h2>' + ('Owned Lean core answers · no fixed reconstruction challenge'
            if core.get('textbook_exercise') else 'Owned Lean example · no fixed reconstruction challenge'
            if owned_original else 'Lean view: not yet aligned') + '</h2>' + lean
        + ('<p>Named owned core answers and their exact domain are separate from full explanatory coverage or a fixed reconstruction challenge.</p>'
           if core.get('textbook_exercise') else
           '<p>The owned declaration proves the concrete witness. This is a reference answer, not a separately aligned Lean task or a score.</p>'
           if owned_original else '<p>This support theorem does not certify the complete QA or its explanatory counterexamples.</p>')
        + '</section>')
    dependencies = ''.join('<h3>' + label + '</h3><ul>' + ''.join('<li><code>' + escape(n) + '</code></li>' for n in core['dependencies'][key]) + '</ul>'
                           for key, label in (('astis', 'ASTIS definitions / proof calls' if bench.has_lean(core) else 'ASTIS formal support (not an equivalent QA)'), ('mathlib', 'Mathlib facts / definitions')))
    support_links = ''
    for support in core.get('supporting_declarations', []):
        support_href, _ = astis_site.source_href(known[support['declaration']], from_path=rel)
        support_links += ('<li><a href="' + escape(support_href) + '"><code>'
                          + escape(support['declaration']) + '</code></a> · LF source SHA-256: <code>'
                          + support['source_sha256_lf'] + '</code></li>')
    if support_links:
        dependencies += '<h3>Additional source-bound support (not full QA certification)</h3><ul>' + support_links + '</ul>'
    related = [g for g in (bench.curriculum.graph_items() if structural is None else structural)
               if g.get('core_id') == core['id'] or
               (g['context']['kind'] == 'compiled-proof-body-constant-occurrences'
                and core['declaration'] in g['context']['nodes'])]
    graph_links=('<p>Structural questions about this proof context (not equivalent mathematical tasks): '+
                 ' · '.join('<a href="'+g['id']+'.html">'+escape(g['title'])+'</a>' for g in related)+'</p>') if related else ''
    graph_position = ('<aside class="sog-graph-position" data-lean-graph-position="' + escape(graph_id or '') + '">'
        '<p class="sog-graph-short">' + graph_short + '<a href="' + escape(href) + '">Source ↗</a>'
        + '<small>' + ('Aligned fixed target' if bench.has_lean(core) else
            'Owned example answer' if owned_original else 'Supporting Lean only') + ' · '
        + anchor_label + '</small></p>'
        + fold('Graph location and verification scope', '<h2>' + escape(declaration.short_name) + '</h2>'
            + prose('Aligned fixed Lean task; its conclusion does not certify every explanatory claim.'
                    if bench.has_lean(core) else 'Library support only: this question has no aligned fixed Lean reconstruction task.')
            + '<p class="sog-caption">A graph location is not a proof-dependency or mathematical-necessity claim. Read the exact scope below.</p>')
        + '</aside>')
    return (f'<article class="sog-reader" {MARKER}><p><a href="index.html">Bench</a> / ' + escape(core['domain']) + '</p>'
        '<div class="eyebrow">' + escape(core['id']) + ' · public-dev · editorial and formal status separate</div><h1>' + escape(core['title']) + '</h1>'
        + '<p>' + escape(domain_names(core)) + ' · ' + escape(' / '.join(t + ': ' + l for t, l in core['track_levels'].items())) + ' (author-assigned; calibration pending)</p>'
        + graph_position
        + exercise_panel(core, checked)
        + '<section><h2>Assumptions and conventions</h2>' + assumptions + '</section>'
        '<section id="natural-language"><h2>Natural-language question</h2>' + prompt_actions(core, 'natural-language', review_row) + prose(core['question'])
        + fold('Reference mathematical proof', proof + fold('How the Lean proof follows these steps' if bench.has_lean(core) else support_title, lean))
        + fold('Assessment rubric · 4 points', rubric) + '</section>'
        + formal_view
        + fold('Why this difficulty?', prose(core['difficulty_reason']))
        + review_panel(core, review_row)
        + graph_links + '<section><h2>What this does—and does not—verify</h2>' + prose(bench.mathematical_scope(core))
        + ('<p>This original worked example does not add a Registry leaf or close any paper theorem.</p>'
           if owned_original else '<p>Existing library mathematics reused; no new mathematical leaf or paper-completion credit.</p>')
        + '<p>The editorial panel records the exact current review scope and remaining unformalized explanation.</p></section>'
        + fold('Sources, graph location and dependencies', prose(core['source_note'])
            + '<p><a href="' + escape(href) + '">Exact local source and full context</a>' + graph_detail
            + '</p><p><code>' + escape(core['declaration']) + '</code></p>'
            + dependencies + '<p>Binding SHA-256: <code>' + core['binding_sha256'] + '</code></p>')
        + '</article>')


def curriculum_page(cores: list[dict]) -> str:
    policy = bench.curriculum.curriculum()
    cover = bench.coverage(cores, bench.curriculum.graph_items())
    editorial = bench.editorial_review(cores)
    rows = []
    for domain, name in policy['domains'].items():
        cells = [c for c in cover['cells'] if c['domain'] == domain]
        values = ''.join('<td>' + ('gap' if c['gap'] else ' / '.join(str(c['draft_views'][t]) for t in ('natural-language', 'lean', 'graph-json'))) + '</td>' for c in cells)
        rows.append('<tr><th><a href="../domains/' + domain + '.html">' + escape(name) + '</a></th>' + values + '</tr>')
    levels = ''.join('<li><a href="../levels/' + key + '.html"><strong>' + key + ' · ' + escape(row['label']) + '</strong></a>' + prose(row['criterion']) + '</li>' for key, row in policy['levels'].items())
    return (f'<article class="sog-reader" {MARKER}><p><a href="../index.html">Bench</a></p><h1>Domains and reasoning levels</h1>'
        '<p>Each cell shows available public-dev views as Natural language / Lean / Graph JSON. On small screens, scroll the table horizontally for L3–L5. A gap is not a proof-completion percentage. Shared questions can occur in several domain indexes but count once globally.</p>'
        '<div class="sog-table"><table><thead><tr><th>Domain</th>' + ''.join('<th>' + l + '</th>' for l in policy['levels']) + '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>'
        '<h2>What the levels mean</h2><ol>' + levels + '</ol>' + prose(policy['difficulty_policy']) + prose(policy['graph_policy'])
        + f'<p>{editorial["accepted_cores"]} of {len(cores)} mathematical cores currently have AI editorial acceptance. Structural editorial status: {escape(cover["graph_editorial_status"])}. Empirical calibration remains open. L5 is a planned research-audit tier, not a claim of solved open problems.</p></article>')


def browse_page(cores: list[dict], key: str, *, domain: bool) -> str:
    policy = bench.curriculum.curriculum()
    title = policy['domains'][key] if domain else key + ' · ' + policy['levels'][key]['label']
    selected = [c for c in cores if key in c['library_domains']] if domain else [c for c in cores if key in c['track_levels'].values()]
    rows = ''.join('<li><a href="../' + c['id'] + '.html">' + escape(c['title']) + '</a> · '
        + escape(' / '.join(t + ': ' + l for t, l in c['track_levels'].items())) + '</li>' for c in selected)
    graphs = [g for g in bench.curriculum.graph_items() if (key in g['library_domains'] if domain else g['level'] == key)]
    graph_rows = ''.join('<li><a href="../' + g['id'] + '.html">' + escape(g['title']) + '</a> · ' + g['level'] + '</li>' for g in graphs)
    introduction = ('<p>Separate sharpness for a specified method from a lower bound for every algorithm in a stated oracle model. '
                    'Read the <a href="../../../lower-bounds/index.html">Lower Bounds research guide</a> for the source and graph context. '
                    'A linked result is not automatically a Bench question or a complete lower-bound proof.</p>'
                    if domain and key == 'lower-bounds' else '')
    return (f'<article class="sog-reader" {MARKER}><p><a href="../curriculum/index.html">Curriculum</a></p><h1>' + escape(title)
        + '</h1>' + introduction + '<h2>Mathematical QA</h2>' + ('<ul>' + rows + '</ul>' if rows else '<p>No authored question at this tier yet. This is an explicit coverage gap.</p>')
        + '<h2>Structural graph QA</h2>' + ('<ul>' + graph_rows + '</ul>' if graphs else '<p>No structural question in this slice yet.</p>')
        + '<p>Difficulty is provisional. Each question discloses its own current editorial status; empirical calibration remains pending.</p></article>')


def graph_page(item: dict, graph_ids: set[str] | None = None) -> str:
    prompt = bench.curriculum.graph_prompts([item])[0]
    evidence = graph_review.summary(bench.curriculum.graph_items())['items'][item['id']]
    status = '<p>Current editorial status: <strong>' + escape(evidence['editorial']) + '</strong>. This is AI review of structural QA, not a theorem or calibrated difficulty.</p>'
    status += '<p>Limits recorded at the time of the review:</p><ul>' + ''.join(
        '<li>' + escape(s) + '</li>' for s in evidence.get('issues', []) + evidence.get('remaining_limits', [])) + '</ul>'
    round_name = evidence.get('review_round', graph_review.CURRENT_ROUND.name)
    status += '<p><a href="downloads/graph-editorial-review.json">Exact review bindings and report hashes</a> · <a href="https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/tree/main/benchmarks/samplingoptimisationgeometrybench/reviews/'+escape(round_name)+'">Independent review for this question</a></p>'
    compiled=item['context']['kind']=='compiled-proof-body-constant-occurrences'
    trace = ''
    lookup = ''
    positions = ''
    if compiled:
        import sog_bench_graph_slices
        artifact=sog_bench_graph_slices.artifact_for(item['id'])
        if 'remove' in item:
            paths, shared = sog_bench_graph_slices.reference_paths(item)
            labels = item['context']['node_labels']
            trace = ''.join('<p>Selected path: ' + escape(' → '.join(labels[n] for n in path))
                            + '.</p>' for path in paths)
            if len(item['targets']) > 1 and shared:
                trace += ('<p>Shared immediate proof-body parent(s): '
                          + escape(', '.join(labels[n] for n in shared))
                          + '. Sharing a parent alone does not imply a directed path between the targets.</p>')
        if evidence['editorial'] in {'accepted', 'accepted-after-repair'} and item['split'] == 'public-dev':
            run_dir = '.astis/sog-bench/runs/' + item['id'] + '-lookup'
            commands = (
                'python tools/sog_bench_graph_search.py run --task-id ' + item['id']
                + ' --max-lookups 8 --output ' + run_dir + '\n'
                + 'python tools/sog_bench_graph_search.py replay --run ' + run_dir
            )
            lookup = fold('Try this as a bounded search task',
                '<p>From the repository root, run the first command and send the emitted prompt to the solver. '
                'It receives the question and the results of its own <code>find</code> or <code>inspect</code> requests, '
                'not the diagram, answer, or repository. Submit one final; invalid lookups spend budget. '
                'The second command replays the recorded interaction.</p>'
                + astis_site.code_html(commands, 'bash')
                + '<p><a href="downloads/EVALUATION.md#graph-lookup-without-the-snapshot">JSONL tool and scoring protocol</a>. '
                'This is a local operator workflow, not live Lean verification or an unseen test.</p>')
        if graph_ids is not None:
            positions = fold('Locate these declarations in the Lean Graph',
                '<p>Open an exact declaration node to inspect its source and wider context. '
                'A node location is not another occurrence edge.</p><ul>' + ''.join(
                    '<li>' + (f'<a href="../../underlying-lean-graph/index.html?focus={quote("decl:" + node, safe="")}">{escape(label)}</a>'
                              if 'decl:' + node in graph_ids else
                              escape(label) + ' · declaration not indexed') + '</li>'
                    for node, label in item['context']['node_labels'].items()) + '</ul>')
    provenance=('<p>This is a recorded source-bound compiler snapshot. CI separately replays the trusted extractor. It is not a fresh Lean run in this browser, a full proof closure or a minimal-premise certificate. Unique proof constants do not count runtime invocations, recursive calls or oracle queries.</p><p><a href="downloads/'+artifact+'">Recorded compiler slice and provenance</a></p>') if compiled else '<p>This graph scans source import declarations, not theorem proof bodies.</p>'
    profiles=''
    if item.get('required_statement_constants'):
        profiles=('<section data-statement-profiles><h2>Statement-occurrence filter</h2><p>Requested constants: '
            + ', '.join('<code>'+escape(n)+'</code>' for n in item['required_statement_constants'])
            + '.</p><p>'+escape(item['context']['statement_profile_scope'])
            + ' Absence here does not mean absence after unfolding or proof derivation.</p>'
            + '<div class="sog-table"><table><thead><tr><th>Selected declaration</th><th>Emitted direct constants</th></tr></thead><tbody>'
            + ''.join('<tr><th>'+escape(item['context']['node_labels'][n])+'</th><td>'
                + (', '.join('<code>'+escape(c)+'</code>' for c in item['context']['statement_profiles'][n]) or 'None of the whitelisted constants; not a claim of no assumptions.')
                + '</td></tr>' for n in item['context']['nodes'])
            + '</tbody></table></div></section>')
    related=[c for c in bench.materialize() if c['id']!=item['core_id'] and c['declaration'] in item['context']['nodes']]
    background=('<p>Related exercises about selected statements: '+ ' · '.join(
        '<a href="'+c['id']+'.html">'+escape(c['title'])+'</a>' for c in related)+'.</p>') if related else ''
    return (f'<article class="sog-reader" {MARKER}><p><a href="graph-json/index.html">Graph QA</a></p><h1>' + escape(item['title']) + '</h1>'
        + '<p>' + item['level'] + ' · public-dev · structural QA, not a theorem proof</p>'
        + '<p><a href="'+item['core_id']+'.html">Read the source mathematical proof and optional Lean</a>. This is context linkage, not an equivalent mathematical question.</p>' + prose(item['question'])
        + '<p>Targets: ' + escape(', '.join(item['context'].get('node_labels',{}).get(n,n) for n in item['targets'])) + '</p>'
        + (prose(('Queried interface: ' if compiled else 'Removed module: ') + item['context'].get('node_labels',{}).get(item['remove'],item['remove'])) if 'remove' in item else '')
        + import_figure(item['context'])
        + profiles
        + background
        + lookup
        + positions
        + fold('Independent structural review and limits', status)
        + fold('Evidence kind and source scope', provenance+prose(item['context']['truth_boundary']))
        + fold('Exact JSON snapshot and response schema',
            '<p>The supplied-snapshot response identifies this visible prompt with <code>prompt_sha256</code>. '
            'The current CLI rejects duplicate JSON keys before scoring; this does not authenticate who answered or when.</p>'
            '<pre><code class="language-json">' + escape(json.dumps(prompt, indent=2)) + '</code></pre>')
        + fold('Reference structural answer · 2 checks, 1 point', trace + '<pre><code>' + escape(json.dumps(item['answer'], indent=2)) + '</code></pre>'
            '<p>One point requires both the exact structural node set and a false mathematical-necessity certification. The constant boundary answer earns no standalone credit. Edges have only the stated evidence kind. Neither a positive path nor an absent induced path proves mathematical necessity or full-closure independence.</p>')
        + '<p>No model score, theorem-equivalence certificate or calibrated difficulty is asserted.</p></article>')


def evaluation_page() -> str:
    return bench_portals.evaluation_page()


def evaluation_guide() -> str:
    prepare = 'python tools/sog_bench_prose.py prepare --submissions responses.jsonl --run-metadata run.json --output .astis/sog-bench/runs/my-run'
    plan = 'python tools/sog_bench_prose.py plan --run-metadata run.json --output .astis/sog-bench/runs/my-plan'
    score = 'python tools/sog_bench_prose.py score --packet .astis/sog-bench/runs/my-run --adjudication completed.json --output .astis/sog-bench/runs/my-run-score.json'
    return (f'<article class="sog-reader" {MARKER}><p><a href="../index.html">Bench</a></p><h1>Run and assess answers</h1>'
        '<p class="lede">Keep the question, first answer and judgment traceable.</p>'
        '<p>Offline human-attested prose scoring is available. The website does not execute model requests or submitted Lean. No model performance has been measured.</p>'
        '<ol><li><strong>Choose first.</strong> Select core IDs, model/version, retrieval policy and tools before collecting answers. Give the model only the prompt-only records.</li>'
        '<li><strong>Freeze the run.</strong> Save raw first responses and metadata. The recorder binds prompts, references, rubric and answers by SHA-256; missing answers stay in the denominator.</li>'
        '<li><strong>Have a human assess it.</strong> Fill each frozen rubric criterion with 0/1 and a reason. The report records those judgments, not automatically verified mathematics or authenticated grader identity.</li></ol>'
        + fold('Commands and input formats',
            '<p>Before collecting answers, seal the selected prompts and run conditions (Python 3.11+):</p><pre><code>' + escape(plan) + '</code></pre>'
            '<p>Keep its digest separately and attach it to the answer archive as described in the full protocol. For an exploratory run without a plan:</p><pre><code>' + escape(prepare) + '</code></pre>'
            '<p>Copy the generated adjudication-template.json to completed.json. An actual human supplies grader identity, timestamp and all four criterion judgments per nonempty answer.</p>'
            '<pre><code>' + escape(score) + '</code></pre>'
            '<p>For double grading, retain both independent worksheets and have a third human resolve only disagreements. Reports distinguish selected cores, equal-weight families and provisional levels.</p>'
            '<p><a href="../downloads/examples/prose-run.json" download>Run-metadata template</a> · <a href="../downloads/EVALUATION.md">Complete recording and scoring instructions</a></p>')
        + fold('Other tracks and scientific limits',
            '<p>Graph JSON has deterministic exact-snapshot scoring; it certifies no mathematical necessity. Lean reference compilation checks trusted references only, not arbitrary submissions.</p>'
            '<p>Human assessments require actual mathematical checking. No keyword grader or unvalidated AI grader is supplied. Run execution, retrieval compliance and human identity are not authenticated by this recorder.</p>'
            '<p>All current tasks are public-dev. These records cannot demonstrate unseen generalization, difficulty calibration or private-family evaluation. A paired core is not two independent samples.</p>'
            '<p><a href="../downloads/FAMILY_ISOLATION.md">Held-out family preflight and limitations</a></p>')
        + '<p><a href="../downloads/reviewed-questions.jsonl" download>Reviewed prompt-only tasks</a> · <a href="../downloads/EVALUATION.md">Full protocol</a> · <a href="../graph-json/index.html">Structural graph QA</a></p></article>')


def graph_index_page(graphs: list[dict]) -> str:
    groups=(('source-scanned-module-imports','Source imports','Arrows record imported modules, not proof-term use.'),
            ('compiled-proof-body-constant-occurrences','Compiled proof bodies','Arrows record selected theorem constants in compiled proof bodies, not necessity or a full closure.'))
    sections=''
    for kind,title,note in groups:
        selected=[g for g in graphs if g['context']['kind']==kind]
        sections+='<section><h2>'+title+'</h2><p>'+note+'</p><ul>'+''.join(
            '<li><a href="../'+g['id']+'.html">'+escape(g['title'])+'</a> · '+g['level']+
            ' · <a href="../'+g['core_id']+'.html">mathematical source context</a></li>' for g in selected)+'</ul></section>'
    return (f'<article class="sog-reader" {MARKER}><p><a href="../index.html">Bench</a></p><h1>Structured graph QA</h1>'
        '<p>Choose the evidence kind before interpreting an arrow. These public-dev structural questions link to mathematical source cores but are not equivalent mathematics tasks or independent held-out samples.</p>'
        +sections+'<p><a href="../downloads/graph-questions.jsonl" download>Prompt-only graph JSONL</a> · <a href="../downloads/graph-reference.jsonl" download>Structural references</a></p>'
        '<p>Prefer the current admitted subset: <a href="../downloads/reviewed-graph-questions.jsonl" download>Reviewed graph prompts</a> · <a href="../downloads/reviewed-graph-reference.jsonl" download>Reviewed graph references</a> · <a href="../downloads/graph-editorial-review.json">Current review evidence</a>.</p></article>')


def import_figure(graph: dict) -> str:
    """Layout a bounded DAG from its real edges; no graph-theoretic proof credit."""
    nodes, edges = graph['nodes'], graph['edges']
    compiled=graph['kind']=='compiled-proof-body-constant-occurrences'
    ranks = {}
    def rank(node, active):
        if node in active:
            raise ValueError('Graph illustration requires an acyclic slice')
        if node not in ranks:
            ranks[node] = max([rank(b, active | {node}) + 1 for a, b in edges if a == node] or [0])
        return ranks[node]
    for node in nodes:
        rank(node, set())
    highest = max(ranks.values(), default=0)
    groups = {r: sorted(n for n in nodes if ranks[n] == r) for r in set(ranks.values())}
    width = max(660, 280 * (max(map(len, groups.values()), default=1) + 1))
    height = 100 + highest * 130
    positions = {n: ((i + 1) * width / (len(group) + 1), 45 + (highest - r) * 130)
                 for r, group in groups.items() for i, n in enumerate(group)}
    labels={n:graph.get('node_labels',{}).get(n,n.rsplit('.',1)[-1]) for n in nodes}
    lines={n:[label] for n,label in labels.items()}
    box_width,box_height=250,44
    if compiled:
        # Keep exact reviewed labels at a readable size instead of shrinking
        # the text. Compact wrapped cards keep a four-node row visible on
        # desktop; mobile retains the existing horizontal scroll.
        lines={n:wrap(label,width=20,break_long_words=False,break_on_hyphens=False)
               for n,label in labels.items()}
        longest=max((len(line) for label in lines.values() for line in label),default=0)
        box_width=max(172,8*longest+14)
        box_height=max(44,15*max(map(len,lines.values()),default=1)+14)
        gap,pitch=20,box_width+20
        columns=max(map(len,groups.values()),default=1)
        width=max(240, pitch*columns-gap+12)
        row_pitch=max(130,box_height+32)
        height=box_height+56+highest*row_pitch
        positions={n:((width-(len(group)*box_width+(len(group)-1)*gap))/2+box_width/2+i*pitch,
                      box_height/2+23+(highest-r)*row_pitch)
                   for r,group in groups.items() for i,n in enumerate(group)}
    half=box_height/2
    style='' if compiled else 'stroke-dasharray="5 4"'

    def arrow(a, b):
        sx, sy = positions[a][0], positions[a][1] + half
        tx, ty = positions[b][0], positions[b][1] - half
        points = [(sx, sy)]
        # A direct reference may skip ranks. Keep an unobstructed straight
        # arrow; otherwise pass each intermediate row through a free lane.
        if compiled and ranks[a] - ranks[b] > 1:
            def straight_x(y):
                return sx + (tx - sx) * (y - sy) / (ty - sy)

            lanes, obstructed = [], False
            for r in range(ranks[a] - 1, ranks[b], -1):
                row = [positions[n] for n in groups[r]]
                y = row[0][1]
                boxes = [(x - box_width/2 - 4, x + box_width/2 + 4) for x, _ in row]
                left, right = sorted((straight_x(y - half), straight_x(y + half)))
                obstructed |= any(left < hi and right > lo for lo, hi in boxes)
                gaps = zip([1, *(hi for _, hi in boxes)], [*(lo for lo, _ in boxes), width - 1])
                desired = straight_x(y)
                lane = min((min(max(desired, lo), hi) for lo, hi in gaps if lo <= hi),
                           key=lambda x: abs(x - desired))
                lanes.extend([(lane, y - half - 8), (lane, y + half + 8)])
            if obstructed:
                points.extend(lanes)
        points.append((tx, ty))
        return 'M ' + ' L '.join(f'{x} {y}' for x, y in points)

    paths = ''.join(f'<path d="{arrow(a, b)}" stroke="#657080" {style} fill="none" marker-end="url(#sog-arrow)"/>' for a, b in edges)
    def box(n,x,y):
        first_y=y+4-(len(lines[n])-1)*7.5
        content=' '.join(f'<tspan x="{x}" dy="{0 if i==0 else 15}">{escape(line)}</tspan>'
                         for i,line in enumerate(lines[n]))
        return (f'<g><title>{escape(n)}</title><rect x="{x-box_width/2}" y="{y-half}" width="{box_width}" height="{box_height}" rx="6" fill="#f5f6f8" stroke="#657080"/>'
                f'<text x="{x}" y="{first_y}" text-anchor="middle" font-size="14" fill="#17212f" aria-label="{escape(labels[n])}">{content}</text></g>')
    boxes=''.join(box(n,x,y) for n,(x,y) in positions.items())
    label='Selected compiled proof-body occurrences; not full closure or mathematical necessity' if compiled else 'Source-scanned import graph; arrows point to imported modules, not theorem implication'
    caption='Solid arrows: selected theorem constants occur in the compiled proof bodies, including proof-term annotations. Other constants and private auxiliaries are omitted; a missing path is not full-closure independence.' if compiled else 'Dashed arrows: source-scanned imports in the supplied slice. The shared module occurs once.'
    return (f'<figure class="sog-graph"><svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" role="img" aria-label="{label}" viewBox="0 0 {width} {height}">'
        '<defs><marker id="sog-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#657080"/></marker></defs>'
        + paths + boxes + '</svg><figcaption>Scroll horizontally on a small screen. '+caption+' Neutral colours make no proof-status claim.</figcaption></figure>')


def enrich_site(output: Path) -> None:
    cores = bench.materialize()
    review_rows = bench.editorial_review(cores)['items']
    known = astis_site._SOURCE_BY_NAME or {d.full_name: d for d in astis_site.scan_project_sources()[1]}
    astis_site._SOURCE_BY_NAME=known
    checked = bench.receipt_current(cores)
    graph_ids = bench.graph_index_ids(output / 'data/underlying-lean-graph.json')
    target = output / HUB
    target.mkdir(parents=True, exist_ok=True)
    bench.export(target / 'downloads', cores, graph_ids=graph_ids)
    bench.archive_bytes(target / 'downloads', target / 'pilot.zip')
    for collection in bench_portals.configuration()['collections']:
        folder = target / collection['id']
        folder.mkdir(parents=True, exist_ok=True)
        for filename, content in bench_portals.collection_assets(target/'downloads',cores,collection).items():
            (folder/filename).write_bytes(content)
    shutil.copyfile(ROOT / 'website/static/sog-bench.css', output / 'assets/sog-bench.css')
    pages = [('index.html', bench_portals.configuration()['display_name'], home(cores))]
    pages += [(c['id']+'/index.html', c['name'], bench_portals.collection_page(cores,c))
              for c in bench_portals.configuration()['collections']]
    graphs = bench.curriculum.graph_items()
    pages += [(track + '/index.html', track.replace('-', ' ').title(), track_page(cores, track)) for track in bench.TRACKS]
    pages += [(c['id'] + '.html', c['title'], core_page(c, checked, graph_ids, known,graphs,review_rows[c['id']])) for c in cores]
    policy = bench.curriculum.curriculum()
    graphs = bench.curriculum.graph_items()
    pages.append(('curriculum/index.html', 'Bench curriculum', curriculum_page(cores)))
    pages.append(('evaluation/index.html', 'Run and assess answers', evaluation_page()))
    pages.append(('evaluation/guide.html', 'Recording and scoring answers', evaluation_guide()))
    pages.append(('training/index.html', 'Training data and task API', training_page()))
    pages.append(('training/guide.html', 'Training and environment guide', training_guide()))
    pages.append(('experts/index.html', 'Expert review and Lean graph positions', experts_page(cores, graph_ids, known)))
    pages.append(('textbook-exercises/index.html', 'Numbered textbook exercises', exercise_index(cores, checked)))
    pages += [('domains/' + key + '.html', title, browse_page(cores, key, domain=True)) for key, title in policy['domains'].items()]
    pages += [('levels/' + key + '.html', key, browse_page(cores, key, domain=False)) for key in policy['levels']]
    pages += [(g['id'] + '.html', g['title'], graph_page(g, graph_ids)) for g in graphs]
    graph_index=graph_index_page(graphs)
    pages.append(('graph-json/index.html', 'Structured graph QA', graph_index))
    for tail, title, body in pages:
        rel = HUB + tail
        text = astis_site.page(title, rel, local_navigation(tail) + body)
        text = source_lineage.canonical_shell(text, rel, output)
        text = text.replace('</head>', '<link rel="stylesheet" href="' + astis_site.relative_prefix(rel) + 'assets/sog-bench.css"></head>')
        astis_site.write_page(output, rel, text)
    # A quiet, independent entry point: no links to unrelated libraries/projects.
    for path in output.rglob('*.html'):
        text = path.read_text(encoding='utf-8')
        if 'data-sog-bench-nav' not in text and '<div class="sidebar-utility">' in text:
            link = astis_site.relative_prefix(path.relative_to(output).as_posix()) + HUB + 'index.html'
            text = text.replace('<div class="sidebar-utility">', '<div class="sidebar-utility"><a data-sog-bench-nav href="' + link + '">QA Bench</a>', 1)
            path.write_text(text, encoding='utf-8', newline='\n')
    source_lineage.append_main(output, 'index.html',
        f'<section data-sog-bench-entry><h2>SamplingOptimisationGeometryBench</h2><p>Explore paired natural-language and Lean QA for sampling, optimisation and geometry. <a href="{HUB}index.html">Open the public development pilot</a>.</p></section>',
        'data-sog-bench-entry')


def exercise_probe_records(cores: list[dict], *, checked: bool) -> dict:
    """Project only the named answers actually covered by the current Bench receipt."""
    if not checked:
        return {}
    import sog_bench_exercises as exercises

    contexts = exercises.compile_contexts(cores)
    return {'decl:' + name: {'source_file': answer['source_file'],
                            'source_line': answer['source_line'],
                            'context_sha256': contexts[name]}
            for name, answer in exercises.answers(cores).items()}


def exercise_probe_detail(record: dict) -> dict:
    return {
        'label': 'Bench compilation (named answer)',
        'value': (f"{record['source_file']}:{record['source_line']} passed the current named-answer "
                  "compiler and axiom probe. This scoped receipt does not change the repository "
                  "badge, proof edges, or source coverage."),
    }


def project_current_exercise_probes(nodes: dict) -> None:
    if not bench.RECEIPT.is_file():
        return
    cores = bench.materialize()
    for ident, record in exercise_probe_records(cores, checked=bench.receipt_current(cores)).items():
        if has_exercise_graph_target(nodes, ident.removeprefix('decl:'), checked=False):
            nodes[ident][OWNED_ANSWER_PROBE] = record
            nodes[ident].setdefault('details', []).append(exercise_probe_detail(record))


def validate_exercise_probes(nodes: dict, expected: dict) -> list[str]:
    actual = {ident: node[OWNED_ANSWER_PROBE] for ident, node in nodes.items()
              if OWNED_ANSWER_PROBE in node}
    return [f'Missing or stale Bench named-answer compilation evidence: {ident}'
            for ident in sorted(actual.keys() | expected.keys())
            if ident not in expected or actual.get(ident) != expected[ident]
            or exercise_probe_detail(expected[ident]) not in nodes[ident].get('details', [])]


def has_exercise_graph_target(nodes: dict, declaration: str, *, checked: bool,
                              probe: dict | None = None) -> bool:
    """Accept a precise source anchor, requiring actual evidence when compiled is claimed."""
    node = nodes.get('decl:' + declaration, {})
    return (node.get('kind') == 'declaration' and bool(node.get('url'))
            and node.get('status') in {'compiled', 'partial'}
            and (not checked or node['status'] == 'compiled'
                 or (probe is not None and node.get(OWNED_ANSWER_PROBE) == probe)))


def validate_site(output: Path) -> list[str]:
    errors = []
    cores = bench.materialize()
    review_rows = bench.editorial_review(cores)['items']
    known = astis_site._SOURCE_BY_NAME or {d.full_name: d for d in astis_site.scan_project_sources()[1]}
    astis_site._SOURCE_BY_NAME=known
    checked = bench.receipt_current(cores)
    graph_path = output / 'data/underlying-lean-graph.json'
    ids = set()
    if graph_path.is_file():
        nodes = {n['id']: n for n in json.loads(graph_path.read_text(encoding='utf-8'))['nodes']}
        ids = set(nodes)
        probes = exercise_probe_records(cores, checked=checked)
        errors.extend(validate_exercise_probes(nodes, probes))
        for core in cores:
            module = core['source_file'].removesuffix('.lean').replace('/', '.')
            if 'decl:' + core['declaration'] not in ids and 'module:' + module not in ids:
                errors.append('Missing Bench graph target: ' + core['id'])
            for answer in core.get('textbook_exercise', {}).get('answer_declarations', []):
                name = answer['declaration']
                if not has_exercise_graph_target(nodes, name, checked=checked,
                                                 probe=probes.get('decl:' + name)):
                    scope = 'compiled ' if checked else ''
                    errors.append('Numbered exercise requires the exact ' + scope + 'owned declaration graph node: ' + answer['declaration'])
    else:
        errors.append('Bench requires the canonical Lean graph')
    policy = bench.curriculum.curriculum()
    graphs = bench.curriculum.graph_items()
    extra = ['curriculum/index.html', 'graph-json/index.html', 'evaluation/index.html', 'evaluation/guide.html', 'training/index.html', 'training/guide.html', 'experts/index.html', 'textbook-exercises/index.html',
             *(c['id']+'/index.html' for c in bench_portals.configuration()['collections']),
             *('domains/' + d + '.html' for d in policy['domains']),
             *('levels/' + l + '.html' for l in policy['levels']), *(g['id'] + '.html' for g in graphs)]
    for collection in bench_portals.configuration()['collections']:
        for filename, content in bench_portals.collection_assets(output/HUB/'downloads',cores,collection).items():
            path = output / HUB / collection['id'] / filename
            if not path.is_file() or path.read_bytes() != content:
                errors.append('Missing or stale Bench collection: '+collection['id']+'/'+filename)
    for rel in ['index.html', *(t + '/index.html' for t in bench.TRACKS), *(c['id'] + '.html' for c in cores), *extra]:
        path = output / HUB / rel
        if not path.is_file() or MARKER not in path.read_text(encoding='utf-8'):
            errors.append('Missing Bench reader: ' + rel)
    current_pages = {'index.html': home(cores), 'evaluation/index.html': evaluation_page(),
                     'evaluation/guide.html': evaluation_guide(),
                     **{c['id']+'/index.html': bench_portals.collection_page(cores,c) for c in bench_portals.configuration()['collections']},
                     'training/index.html': training_page(), 'training/guide.html': training_guide(), 'experts/index.html': experts_page(cores, ids, known),
                     'textbook-exercises/index.html': exercise_index(cores, checked),
                     'graph-json/index.html':graph_index_page(graphs),
                     'curriculum/index.html': curriculum_page(cores),
                     **{'domains/' + d + '.html': browse_page(cores, d, domain=True) for d in policy['domains']},
                     **{'levels/' + l + '.html': browse_page(cores, l, domain=False) for l in policy['levels']},
                     **{g['id'] + '.html': graph_page(g, ids) for g in graphs}}
    for rel, body in current_pages.items():
        path = output / HUB / rel
        if path.exists() and body not in path.read_text(encoding='utf-8'):
            errors.append('Stale Bench curriculum or structural graph: ' + rel)
    for core in cores:
        path = output / HUB / (core['id'] + '.html')
        if path.is_file() and core_page(core, checked, ids, known,graphs,review_rows[core['id']]) not in path.read_text(encoding='utf-8'):
            errors.append('Stale Bench mathematics or compiler label: ' + core['id'])
    # Recreate the deterministic export and compare bytes, not manually copied counts.
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        export = Path(tmp) / 'export'
        bench.export(export, cores, graph_ids=ids)
        for source in export.rglob('*'):
            if source.is_file():
                target = output / HUB / 'downloads' / source.relative_to(export)
                if not target.is_file() or target.read_bytes() != source.read_bytes():
                    errors.append('Stale Bench export: ' + source.relative_to(export).as_posix())
        archive = Path(tmp) / 'pilot.zip'
        bench.archive_bytes(export, archive)
        published = output / HUB / 'pilot.zip'
        if not published.is_file() or published.read_bytes() != archive.read_bytes():
            errors.append('Missing or stale Bench archive')
    return errors
