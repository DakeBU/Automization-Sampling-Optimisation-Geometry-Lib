from pathlib import Path
import hashlib,json
base=Path('runs/20261007-companion-priority')
pre69=base/'pbps-reflection-rotation-preproof69'
pre=base/'pbps-actual-projected-rotation-preproof70';pre.mkdir(exist_ok=False)
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
old=(pre69/'header0-expanded.lean').read_text(encoding='utf-8')
assert old.count('theorem actual_reflection_intertwining')==1
old=old.replace('theorem actual_reflection_intertwining','theorem actual_projected_rotation',1)
ending='‖f‖^2=‖fP‖^2+‖fperp‖^2 ∧ ‖fV‖≤‖fperp‖)'
assert old.count(ending)==1
new=old.replace(ending,'''‖f‖^2=‖fP‖^2+‖fperp‖^2 ∧ ‖fV‖≤‖fperp‖ ∧
                              let g : Lp ℝ 2 J := U (P f-(f-P f))
                              (∫ z, g z ∂J)=0 ∧
                              ∃ gP : HP0,
                                HP0.subtypeL gP=condExpL2 ℝ ℝ (μ:=J) measurable_snd.comap_le g ∧
                                let gperp : Hperp := R g
                                let gV : HP0 := V0.adjoint gperp
                                gP=A0 fP-ΓP0 fV ∧
                                gV=ΓP0 fP+A0 fV ∧
                                ‖gP‖^2+‖gV‖^2=‖fP‖^2+‖fV‖^2)''')
(pre/'header0-proposed-expanded.lean').write_text(new,encoding='utf-8',newline='\n')
graph=pre69/'independent-primary69/source-proof-graph.json'
payload=dict(schema='raw-next-source-header-proposal70-not-sealed-not-claimed-v1',status='RAW_SOURCE_BACKED_PROPOSAL_NOT_ADMITTED',
 parent_candidate='AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionIntertwining.actual_reflection_intertwining',
 parent_status='Local compiled; independent math/source reviews currently pending; not independently VERIFIED.',
 source_graph=dict(path=graph.as_posix(),raw_sha256=sha(graph.read_bytes())),source_nodes=['P12','P13','P14'],
 proposed_module='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean',
 proposed_decl='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation.actual_projected_rotation',
 exact_delta='For SAME actual original globally centered f and SAME g=U(P-Pperp)f, derive mean(g)=0, actual conditional gP and polar gV with gP=A0fP-Gamma0fV and gV=Gamma0fP+A0fV, plus the exact two-component energy identity.',
 actual_components_not_defined_as_rhs=True,no_new_public_condition_mean_g=True,no_sharp_energy68_proof_dependency=True,
 source_consumers=['P16/P17 actual B21 corrector change','P19 B4 actual comparator'],
 proposed_header_RAW_sha256=sha((pre/'header0-proposed-expanded.lean').read_bytes()),
 remaining_boundary='P16 same corrector algebra and actual B21 change remain next; B4/H1/dynamics/main/errors/cost/composition independent.',
 source_only_expectations_reuse_required=True,statement_seal=False,SAU_claim=False,proof_search=False,compiled_target=False,Goal_complete=False)
(pre/'proposal.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Wrote raw source-backed actual rotation70 header proposal; no Statement Seal, SAU claim or proof credit.')
