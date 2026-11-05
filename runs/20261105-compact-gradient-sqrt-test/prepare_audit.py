"""Freeze actual compiler/source context; generate NO independent verdict."""
import json
from pathlib import Path
from tools import astis_publication as publication
from tools import astis_semantic_roundtrip_core as core

stem='compact-gradient-sqrt-test'
audit_id='ASTIS-RT-20261105-CompactGradientSqrtTest'
item=json.loads(Path(f'website/content/publications/{stem}.json').read_text(encoding='utf-8'))['items'][0]
lesson=json.loads(Path(f'website/content/declaration_lessons/{stem}.json').read_text(encoding='utf-8'))['units'][0]
binding=item['bindings'][0]
raw=Path('.astis/sog-bench/compact-gradient-sqrt-elaborated.log').read_text(encoding='utf-8').strip()
prefix='@'+binding['declaration']+' :'
assert raw.startswith(prefix) and 'error:' not in raw
statement=raw[len(prefix):].strip()
assert statement.startswith('∀') and '{E : Type' in statement
focused=Path('.astis/sog-bench/compact-gradient-sqrt-focused.log').read_text(encoding='utf-8')
hilbert=Path('.astis/sog-bench/compact-gradient-sqrt-hilbert-final.log').read_text(encoding='utf-8')
assert 'Build completed successfully (2679 jobs).' in focused and 'error:' not in focused
assert 'error:' not in hilbert and 'depends on axioms:' in hilbert
audit={
    'id':audit_id,'state':'draft',
    'source':{'source_id':item['id'],'anchor':item['source']['anchor'],
        'original_text':lesson['statement'],'text_sha256':core.sha256_text(lesson['statement']),
        'url':item['source']['url']},
    'lean':{'declaration':binding['declaration'],'file':lesson['source_file'],
        'statement':statement,'statement_sha256':core.sha256_text(statement),
        'compiled':True,'formalizer':'agent-task:/root',
        'compiler_evidence':'Owning module/focused test Lake build PASS2679. Fresh direct updated Hilbert test exits0 and prints standard3 axioms; no original energy integrability premise. Only local proof evidence, not independent review/integration.',
        'decoder_context':[
            'ContDiff ℝ ∞ means arbitrarily many continuous Frechet derivatives. The smooth infinity order is distinct from the analytic omega top in Mathlib.',
            'fderiv ℝ f x is the totalized Frechet derivative, a continuous real linear map. Its norm is the operator norm. The displayed genuine smoothness premise is not inferred from that totalization.',
            'HasCompactSupport h means the closure of the set on which h is nonzero is compact. It does not say the whole domain is compact.',
            'MemLp u 2 mu includes a.e. strong measurability and finite squared-integral norm. Integrable includes a.e. strong measurability and finite integral norm. IsFiniteMeasure mu means finite total mass, not mass one.',
            'Real.sqrt is the nonnegative square root, totalized for negative arguments. Real.log and the Bochner integral have totalized off-domain values; explicit Integrable conclusions assert actual finiteness.',
            '𝓝 0 is the ordinary two-sided real neighborhood filter, including zero. The notation ∀ᶠ denotes eventual truth in that filter. OpensMeasurableSpace means all norm-open sets are measurable.'
        ]},
    'publication_binding_sha256':publication.binding_digest(item,binding),
    'publication_context':publication.review_context(item,binding),
    'source_review':{'state':'pending'},'repairs':[]
}
path=Path('research-wiki/semantic-roundtrip/audits')/(audit_id+'.json')
assert not path.exists(),'Never overwrite an existing audit'
core._write_packet(audit,str(path))
packet=core.decoder_packet(audit)
output=Path('runs/blind')/(packet['packet_id']+'.json')
assert not output.exists(),'Never overwrite blind input'
core._write_packet(packet,str(output))
print(json.dumps({'audit':audit_id,'decoder_input':output.as_posix(),
    'packet_sha256':packet['packet_sha256'],'publication_binding_sha256':audit['publication_binding_sha256']}))
