from pathlib import Path
r=Path('runs/20261007-companion-priority/pbps-actual-bounded-gibbs-duality106');s=(r.parent/'pbps-actual-countable-endpoint105/prepare_integration105.py').read_text().replace('105','106')
s=s.replace('ActualCountableEndpointLaw','ActualBoundedGibbsDuality').replace('ActualNormalizedEndpointSector','ActualCountableEndpointLaw').replace('pbps.actualCountableEndpointLaw','pbps.actualBoundedGibbsDuality')
s=s.replace('Actual PBPS countable endpoint probability and reversal','Actual PBPS bounded signed Gibbs duality and fixed-time invariance').replace('arXiv2609.06905v1 Appendix A.1 A7 and nonnegative Gibbs averaging before A8','arXiv2609.06905v1 Appendix A.1 final bounded signed bilinear identity and Gibbs stationarity').replace('Actual countable endpoint law; no SALD claim','Actual bounded duality and fixed-time invariance; no SALD claim')
a=s.index("note = f'");b=s.index('\n\nblock =',a)
s=s[:a]+'''note = f'Independent science {science}. Under the original six assumptions, one global jointly measurable actual PBPS process retains its exact arc/fallback/zero-time contract. For every y,r,T its endpoint pushes the actual Gibbs phase law times countable exponential clocks to the same Gibbs phase law. For every pair of bounded Borel real F,G, both outer tests are integrable and integral F op(G) equals integral (G composed R) op(F composed R). Actual105, actual normalization103 and UnitExponentialProduct are the three direct producers. Momentum symmetry and signed Fubini are internally discharged. The selected direct-marginal proof and printed F=1 route have separate independently admitted source graph alternatives. L2 operators/domains, restart/Markovness, separate kernel witness identification, hypocoercivity, errors, actual expected costs, full composition and all four full papers remain open.'
''' +s[b:]
a=s.index("assert b.count(b'formalizedTechnicalLemmaCount");b=s.index("prefix = f'''",a)
s=s[:a]+'''matches = re.findall(rb'formalizedTechnicalLemmaCount = (\\d+)', b)
assert len(matches) == 1
before_count = int(matches[0]); after_count = before_count + 1
p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = ' + matches[0], b'formalizedTechnicalLemmaCount = ' + str(after_count).encode(), 1))
''' +s[b:]
a=s.index("prefix = f'''");b=s.index('\n\ndef prepend',a)
s=s[:a]+'''prefix = f\'''## Actual PBPS bounded Gibbs duality and fixed-time invariance (2026-10-12)

Independent science {science}. Under the original six analytic assumptions,
one global jointly measurable actual process Z retains its exact live-arc,
raw fallback and parameterwise almost-sure zero-time contract. For every y,r
and finite nonnegative T, endpoint(z,w)=Z(y,r,z,T,w) is measurable and sends
the actual Gibbs phase law nu_y times the countable exponential law P to nu_y.
For all bounded Borel real F,G with finite nonnegative bounds, both outer tests
are integrable and integral F op_T(G) dnu_y equals
integral (G composed R) op_T(F composed R) dnu_y, with R(x,p)=(x,-p).

Actual105 supplies the same global process and endpoint-pair reversal.
Actual normalization103 and UnitExponentialProduct provide the exact input
probabilities. Gaussian negation gives R_*nu_y=nu_y. The direct-marginal route
identifies the endpoint law; finite test bounds justify signed Fubini and
both outer L1 conclusions. The original printed F=1 source route is retained
as an alternative, with the selected extra source edge independently reviewed.
The effective source graph has62 nodes123 edges, without a new source premise.

Eight adjacent formula/Lean regions explain the ASTIS completion. Header,
whole mathematics, fresh blind decoding and primary-first source/exposition
reviews have passed. L2 operator/domain identity, restart/Markovness,
identification with a separate existential kernel witness, hypocoercivity,
implementation errors, actual expected costs and full composition remain red.
Full paper completion remains0/4. The original sole SAU94 lane handles public
integration; actual browser acceptance, main merge and purification retain
separate evidence.

\'''
''' +s[b:]
s=s.replace("anchor = b'#actual-normalized-pbps-endpoint-pair-sector-reversal-2026-10-12'", "anchor = b'#actual-pbps-countable-endpoint-law-2026-10-12'")
s=s.replace("b'#actual-pbps-countable-endpoint-law-2026-10-12', 1", "b'#actual-pbps-bounded-gibbs-duality-and-fixed-time-invariance-2026-10-12', 1")
s=s.replace('Actual countable endpoint law106','Actual bounded Gibbs duality106').replace("print('Verified countable endpoint child admitted through existing sole lane; Registry557; aggregate gates pending.')", "print(f'Verified bounded duality child admitted through existing sole lane; Registry{after_count}; aggregate gates pending.')")
(r/'prepare_integration106.py').write_text(s,encoding='utf8',newline='\n')
