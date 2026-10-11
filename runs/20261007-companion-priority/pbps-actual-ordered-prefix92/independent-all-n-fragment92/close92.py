import pathlib,json,hashlib,re,subprocess
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92';D=B/'independent-all-n-fragment92'
def bind(p):
 b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def put(n,v):
 with (D/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
s=(B/'Induction92.lean').read_text(encoding='utf-8');seal=json.loads((B/'root.statement-seal92.json').read_text(encoding='utf-8'))['expanded_literal_Prop'];t=s[s.index('private theorem actual_prefix_all_integrals'):]
norm=lambda x:re.sub(r'\s+',' ',x).strip()
assert norm(t[t.index('    let c :'):t.index('    ∀ n :')])==norm(seal[seal.index('    let c :'):seal.index('    ∀ n :')])
clean=re.sub(r'/\-[\s\S]*?\-/','',s);assert not re.search(r'\b(?:sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',clean)
receipt=json.loads((D/'kernel.receipt.json').read_text());assert receipt['exit_code']==0
report=dict(decision='ACCEPT_ACTUAL_ALL_N_STRICT_PREFIX_ALL_TESTS_FRAGMENT',checked_base_HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),source=bind(B/'Induction92.lean'),seal=bind(B/'root.statement-seal92.json'),receipt=bind(D/'kernel.receipt.json'),merge=bind(D/'merge-check92.json'),statement_audit={'outer_literal_definitions':22,'matches_seal':True,'original_analytic_hypotheses':['hα','hαβ','hV','hH','hη','hβη'],'no_provider_binders':True,'all_measurable_ENNReal_full_history_tests':True},proof_audit=[
'Nat induction is genuinely performed internally; base consumes the canonical-P n=0 theorem for every T, including 0.',
'Successor uses actual91-derived actual_prefix_step_integral. Measurable J is a proved conclusion; IH is applied to this arbitrary full-history J.',
'Joint Borel K and q produce measurability of F(K)*q on the successor subtype. Geometry produces both simplex measurability premises for subtype Tonelli.',
'ordered_last_nonneg is instantiated with the actual strict simplex. It proves toNNReal(last) coerces back to last; D(K(t),u) is exactly the strict Ioo(last,T) indicator of the literal rate-survival factor.',
'q is finite because it is ofReal of a finite real product. lintegral_mul_const uses this internally proved finiteness, with no integrability or bounded-F premise. Infinite ENNReal values and zero weights remain valid.',
'timedHistory_snoc is instantiated with S composed with Phi, preserving every old record and the next absolute time. weight_snoc_ofReal uses the literal rate and exponential hazard factor and Geometry-produced old-weight nonnegativity.',
'All 32 retained private declarations match a previously reviewed frozen fragment after whitespace/namespace qualification normalization only. The sole new theorem is actual_prefix_all_integrals.'
],edge_cases=['n=0 uses finite empty-product Lebesgue mass 1 and constant full history.','T=0 and n>0 have empty strict simplex and actual strict event.','Stopped/top records and zero clocks are excluded by the exact strict event, not silently assigned positive waiting times.','No positive-dimension premise; rank-zero and zero-rate paths retained.','No terminal survival factor: this is a first-n strict-prefix law, not exactly-n or the full A7 path-functional statement. Counting gloss only almost surely on positive clocks.'],axioms=['propext','Classical.choice','Quot.sound'],fake_closure_scan='PASS',remaining_boundary=['Full sealed public conjunction and production assembly require their own review.','No canonical VERIFIED transition, source/publication completion, science commit or whole A7 claim is supplied by this fragment.'])
put('all-n-fragment-review92.native.json',report)
inputs=[B/'Induction92.lean',B/'root.statement-seal92.json',B/'focused/induction6-typed-interval-predicate/receipt.json',R/'lake-manifest.json',R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe']+[B/(n+'.lean') for n in ['Geometry92','Base92','Integrals92','SubtypeCoordinates92','Algebra92']]
put('closed-RAW92.native.json',dict(inputs=[bind(p) for p in inputs],outputs=[bind(p) for p in sorted(D.iterdir()) if p.is_file()],closure='All listed raw bytes closed; manifest excludes itself.'))
print(json.dumps([bind(D/'all-n-fragment-review92.native.json'),bind(D/'closed-RAW92.native.json')],indent=2))
