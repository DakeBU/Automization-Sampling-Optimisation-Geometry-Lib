"""Pure bounded DOM comparison; no browser, network or canonical writes."""
import hashlib
import json
import sys
sys.dont_write_bytecode = True
from bounded_dom import parse, Node


def sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def compare(html_text, expected):
    root = parse(html_text)
    public_identity = expected['code_panels'][0]['data_inline_lean']
    articles = root.descendants('article', 'data-authored-declaration', public_identity)
    scope = articles[0] if len(articles) == 1 else root
    panels = scope.descendants(attr='data-lean-code-panel')
    actual = []
    for panel in panels:
        code = panel.direct_code()
        actual.append(dict(identity=panel.attrs.get('data-inline-lean'),
                           tag=panel.tag, initially_closed='open' not in panel.attrs,
                           code=code.text() if code else None,
                           direct_code_present=code is not None))
    # Restrict to this one declaration's two exact identities, not whole page.
    ids = {p['data_inline_lean'] for p in expected['code_panels']}
    actual = [p for p in actual if p['identity'] in ids]
    panel_checks = []
    for i, exp in enumerate(expected['code_panels']):
        got = actual[i] if i < len(actual) else None
        ok = bool(got and got['identity'] == exp['data_inline_lean'] and
                  got['tag'] == 'details' and got['initially_closed'] and
                  got['direct_code_present'] and got['code'] == exp['text'])
        panel_checks.append(dict(panel=exp['panel'], exact=ok,
            expected_sha256=exp['LF_UTF8_sha256'],
            actual_sha256=sha(got['code']) if got and got['code'] is not None else None,
            initially_closed=got['initially_closed'] if got else None))
    helper_nested = False
    if len(actual) == 3:
        candidates = [p for p in panels if p.attrs.get('data-inline-lean') in ids]
        cur = candidates[2].parent
        while cur is not None:
            if cur is candidates[1]:
                helper_nested = True
                break
            cur = cur.parent
    steps = [p for p in scope.descendants('div') if p.class_has('proof-reader-step')]
    # An entire chapter may contain other units. Identify this six-step unit by
    # exact expected titles; no inference from unrelated steps.
    own_steps = []
    for p in steps:
        headings = p.descendants('h4')
        heading = headings[0].text() if headings else ''
        if any(heading == e['title'] or heading.endswith(e['title']) for e in expected['BODY_steps']):
            own_steps.append(p)
    body_checks = []
    for i, exp in enumerate(expected['BODY_steps']):
        got = own_steps[i] if i < len(own_steps) else None
        details = got.descendants('details') if got else []
        code = details[0].direct_code() if details else None
        formula_nodes = [p for p in got.descendants('div') if p.class_has('proof-reader-equation')] if got else []
        body_checks.append(dict(step=exp['step'], lines=exp['lines'],
            code_exact=bool(code and code.text() == exp['code']),
            actual_code_sha256=sha(code.text()) if code else None,
            expected_code_sha256=exp['code_LF_UTF8_sha256'],
            formula_exact=bool(formula_nodes and formula_nodes[0].text() == '\\[' + exp['formula'] + '\\]'),
            initially_closed=bool(details and 'open' not in details[0].attrs)))
    claims = [p for p in scope.descendants('p') if p.class_has('reader-claim')]
    ledgers = [p for p in scope.descendants('details') if p.class_has('assumption-ledger')]
    assumptions = [p.text() for p in ledgers[0].descendants('li')] if ledgers else []
    return dict(authored_article_count=len(articles), scoped_panel_count=len(actual), panel_checks=panel_checks,
                helper_nested_in_public_proof=helper_nested,
                scoped_BODY_count=len(own_steps), BODY_checks=body_checks,
                complete_natural_statement_exact=bool(claims and claims[0].text() == expected['complete_natural_statement']),
                full_assumptions_exact=assumptions[:len(expected['assumptions'])] == expected['assumptions'],
                assumptions_initially_closed=bool(ledgers and 'open' not in ledgers[0].attrs),
                no_visual_or_callback_or_download_acceptance=True)
