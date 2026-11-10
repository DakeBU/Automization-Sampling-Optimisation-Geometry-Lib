"""Collect one real model candidate as data only. Never calls Lean or Docker."""
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import sog_bench_lean_stdio as bridge

SEED = 6015
TOKENS = 192
MODEL = 'Qwen/Qwen2.5-0.5B-Instruct'
REVISION = '7ae557604adf67be50417f59c2c2f167def9a775'
WEIGHT = 'fdf756fa7fcbe7404d5c60e26bff1a0c8b8aa1f72ced49e7dd0210fe288fb7fe'
ASSETS = HERE.parent / 'local-models/qwen2.5-0.5b-7ae55760'
PIN = HERE.parent / 'public-graph-qwen2.5-0.5b-first-pilot/preflight.json'
PACKET = HERE / 'v030-local-model-fixed-target-packet/sogb-015'
OUT = HERE / 'v030-local-model-fixed-target-first-candidate'
MARKER = '  -- Replace this comment with your proof.\n'


def digest(path):
    with path.open('rb') as file:
        return hashlib.file_digest(file, 'sha256').hexdigest()


def write(name, payload):
    with (OUT / name).open('xb') as file:
        file.write(payload)


def main():
    os.environ.update(HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1', HF_HUB_DISABLE_TELEMETRY='1')
    files = {p.name: digest(p) for p in ASSETS.iterdir() if p.is_file()}
    assert files == json.loads(PIN.read_bytes())['model_files_sha256']
    assert files['model.safetensors'] == WEIGHT
    packet = bridge.runtime.checked_packet(PACKET)
    template = (PACKET / 'agent/Solution.lean.txt').read_bytes()
    prompt = (PACKET / 'agent/prompt.json').read_bytes()
    assert template.decode().endswith(MARKER)
    task = json.loads(prompt)
    body = template.decode().removesuffix(MARKER)
    instruction = (
        'Complete only the proof body after the final ":= by" in the following Lean 4 file. '
        'Output only Lean tactics as plain text. Start every tactic line with two spaces. '
        'Do not repeat the theorem, use Markdown fences, or use sorry, admit, axioms or placeholders.'
    )
    messages = [{'role': 'system', 'content': instruction},
                {'role': 'user', 'content': body}]
    OUT.mkdir(exist_ok=False)
    write('adapter.py', Path(__file__).read_bytes())
    write('prompt.json', prompt)
    write('Solution.lean.txt', template)
    selection = {'kind': 'declared-model-candidate-only', 'id': packet['id'], 'family': task['family'],
                 'split': task['split'], 'selected': 1, 'binding_sha256': packet['binding_sha256'],
                 'template_sha256': bridge.bench.sha(template), 'prompt_sha256': bridge.bench.sha(prompt),
                 'adapter_sha256': digest(OUT/'adapter.py'), 'model': MODEL, 'revision': REVISION,
                 'asset_sha256': files, 'max_new_tokens': TOKENS, 'seed': SEED,
                 'environment': {k: version(k) for k in ('torch', 'transformers', 'safetensors')},
                 'decoding': 'greedy CPU float32, deterministic; one raw body; no repair',
                 'rendering': 'remove the one fixed placeholder then append raw generated text without edits',
                 'messages': messages}
    write('selection.json', bridge.bench.encoded(selection))
    print('Preselected candidate:', digest(OUT/'selection.json'), flush=True)
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    torch.set_num_threads(4)
    torch.set_num_interop_threads(1)
    torch.manual_seed(SEED)
    torch.use_deterministic_algorithms(True)
    tokenizer = AutoTokenizer.from_pretrained(ASSETS, local_files_only=True, trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(ASSETS, local_files_only=True, trust_remote_code=False,
        use_safetensors=True, dtype=torch.float32, attn_implementation='eager').eval()
    input_ = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True,
                                          return_dict=True, return_tensors='pt')
    with torch.inference_mode():
        output = model.generate(**input_, max_new_tokens=TOKENS, do_sample=False,
                                num_beams=1, pad_token_id=tokenizer.pad_token_id)
    input_ids = input_['input_ids'][0].tolist()
    generated_ids = output[0, len(input_ids):].tolist()
    raw = tokenizer.decode(generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)
    source = body + raw
    frame = bridge.line({'action':'submit', 'source':source})
    assert bridge.request(frame) == {'action': 'submit', 'source': source}
    write('generated.txt', raw.encode('utf-8'))
    write('generated-tokens.json', bridge.bench.encoded({'input_ids': input_ids, 'output_ids': generated_ids}))
    write('candidate.lean.txt', source.encode('utf-8'))
    write('first-submit.jsonl', frame)
    report = {'kind': 'observed-model-candidate-unverified', 'id': task['id'],
              'native_verification': 'not-run', 'score': None, 'provider_calls': 0,
              'generated_tokens': len(generated_ids), 'at_output_budget': len(generated_ids) == TOKENS,
              'files_sha256': {p.name: digest(p) for p in OUT.iterdir() if p.is_file()}}
    write('receipt.json', bridge.bench.encoded(report))
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
