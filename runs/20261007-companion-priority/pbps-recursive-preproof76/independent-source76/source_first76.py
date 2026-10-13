"""Bounded source-only freeze. No candidate76 Lean/header or review decisions read."""
import sys
sys.dont_write_bytecode = True
import os, json, re, html, hashlib, datetime
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path("E:/Samplinglib")
OWN = ROOT / "runs/20261007-companion-priority/pbps-recursive-preproof76/independent-source76"
PLAN = ROOT / "runs/20261007-companion-priority/pbps-recursive-path-preread76"
PRIMARY = ROOT / "runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html"
OWN.mkdir(parents=True, exist_ok=True)
assert not (OWN / "lease.final.json").exists(), "closed owned directory"
def sha(b): return hashlib.sha256(b).hexdigest()
def rawpin(b):
    lf = b.replace(b"\r\n", b"\n")
    return {"RAW_bytes":len(b),"RAW_sha256":sha(b),"LF_bytes":len(lf),"LF_sha256":sha(lf),"LF_recipe":"Only bytewise CRLF -> LF; preserve bare CR and all other bytes."}
def write(name, obj):
    b=(json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf-8")
    (OWN/name).write_bytes(b)
    return {"path":str((OWN/name).relative_to(ROOT)).replace("\\","/"),**rawpin(b)}
def readable(b):
    s=b.decode("utf-8")
    math=[]
    def stash(m):
        math.append("$"+html.unescape(m.group(1))+"$")
        return " MATHPLACEHOLDER%06d "%(len(math)-1)
    s=re.sub(r'<math\b[^>]*\balttext="([^"]*)"[^>]*>.*?</math>',stash,s,flags=re.S)
    s=html.unescape(re.sub(r"<[^>]*>"," ",s))
    for i,value in enumerate(math): s=s.replace("MATHPLACEHOLDER%06d"%i,value)
    return " ".join(s.split())
inputs=[]
def snapshot(path,label):
    b=path.read_bytes()
    dest=OWN/"inputs"/label
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(b)
    inputs.append({"original_path":str(path.relative_to(ROOT)).replace("\\","/"),"snapshot_path":str(dest.relative_to(ROOT)).replace("\\","/"),**rawpin(b)})
    return b
primary=snapshot(PRIMARY,"primary-pbps.exactraw.snapshot.html")
assert len(primary)==1482128 and sha(primary)=="d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760"
plan={}
for name in ["selected.contract.json","source-first.expectations.json","source-proof-graph.json","source.coverage.json","source.regions.json"]:
    plan[name]=json.loads(snapshot(PLAN/name,name))
oldinv=plan["source.coverage.json"]
regions=plan["source.regions.json"]["regions"]
checks={"primary_pin":True,"all_original_regions_exact":True,"all_original_partitions_exact":True,"all_original_items_exact":True,"source_items_distinct":True}
partition_count=0
for region in regions:
    raw=snapshot(ROOT/region["input"]["path"],"regions/"+region["id"]+".exactraw.html")
    lo,hi=region["primary_RAW_range"]
    assert raw==primary[lo:hi]
    assert sha(raw)==region["input"]["RAW_sha256"] and len(raw)==region["input"]["RAW_bytes"]
    cur=lo
    for part in region["complete_byte_partition"]:
        a,b=part["primary_RAW_range"]
        assert a==cur and a<b and sha(primary[a:b])==part["RAW_sha256"]
        cur=b; partition_count+=1
    assert cur==hi
assert len({x["item"] for x in oldinv["items"]})==90
literal_diffs=[]
for item in oldinv["items"]:
    a,b=item["primary_RAW_range"]; raw=primary[a:b]
    assert len(raw)==item["RAW_bytes"] and sha(raw)==item["RAW_sha256"]
    if item["formula_alttext"] is not None:
        m=re.search(rb'\balttext="([^"]*)"',raw)
        assert m and html.unescape(m.group(1).decode("utf-8"))==item["formula_alttext"]
    got=readable(raw)
    if got!=" ".join(item["literal"].split()):
        literal_diffs.append({"item":item["item"],"preread_literal":item["literal"],"independent_primary_rendering":got})

# Expand only the literal definition used by A.1 and repair an excluded bibliographic locator.
extra_specs=[("S2.SS1.p1.4",rb'<p id="S2.SS1.p1.4".*?</p>',"reflection-literal","NODE"),
             ("S2.SS1.p1.m8",rb'<math id="S2.SS1.p1.m8".*?</math>',"reflection-literal","NODE"),
             ("S2.E4.m1",rb'<math id="S2.E4.m1".*?</math>',"reflection-literal","NODE"),
             ("bib.bib16",rb'<li id="bib.bib16".*?</li>',"Davis1984-bibliographic-corrected","EXCLUDED")]
extras=[]
for ident,pattern,region,classification in extra_specs:
    m=re.search(pattern,primary,re.S); assert m
    raw=m.group(0); alt=re.search(rb'\balttext="([^"]*)"',raw) if raw.startswith(b"<math ") else None
    extras.append({"item":ident,"region":region,"primary_RAW_range":[m.start(),m.end()],"tag":"math" if alt else ("li" if ident.startswith("bib.") else "p"),"formula_alttext":html.unescape(alt.group(1).decode("utf-8")) if alt else None,"literal":readable(raw),"classification":classification,"RAW_bytes":len(raw),"RAW_sha256":sha(raw),"source_url":"https://arxiv.org/html/2609.06905v1","role":"literal-definition" if classification=="NODE" else "excluded-bibliographic-context"})
newregions=[]
for ident,pattern in [("reflection-literal",rb'<p id="S2.SS1.p1.4".*?</p>\s*<table id="S2.E4".*?</table>'),("Davis1984-bibliographic-corrected",rb'<li id="bib.bib16".*?</li>')]:
    m=re.search(pattern,primary,re.S); assert m
    path=OWN/"inputs"/"regions"/(ident+".exactraw.html")
    path.write_bytes(m.group(0))
    newregions.append({"id":ident,"primary_RAW_range":[m.start(),m.end()],"snapshot_path":str(path.relative_to(ROOT)).replace("\\","/"),**rawpin(m.group(0))})
assert b'href="#bib.bib16"' in primary[564117:564876]

callers=[
 {"id":"hα","statement":"0 < α","source_items":["S1.p1.m4"]},
 {"id":"hαβ","statement":"α ≤ β","source_items":["S1.p1.m4"]},
 {"id":"hV","statement":"V ∈ C² on the whole finite-dimensional real inner-product space","source_items":["S1.p1.m3"]},
 {"id":"hH","statement":"For every x and v, α * ‖v‖² ≤ inner (Hess V x v) v and inner (Hess V x v) v ≤ β * ‖v‖²","source_items":["S1.E1.m1"]},
 {"id":"hη","statement":"0 < η","source_items":["S2.SS2.p1.m1"]},
 {"id":"hβη","statement":"β * η ≤ 1","source_items":["S2.SS2.p1.m1"]}]
typing=["NormedAddCommGroup E","InnerProductSpace ℝ E","FiniteDimensional ℝ E","MeasurableSpace E","BorelSpace E"]
definitions=[
 {"id":"center","formula":"c(y,xRef) = y − η • gradient V xRef","source_items":["S3.E4.m1"],"semantics":"One actual center; fixed y and xRef throughout every finite history."},
 {"id":"residual","formula":"h(xRef,x) = gradient V x − gradient V xRef","source_items":["S3.E4.m1"],"semantics":"Actual gradient difference, never a supplied arbitrary residual or Lipschitz field."},
 {"id":"reflection","formula":"R_a p = p − (2 * inner a p / ‖a‖²) • a for a ≠ 0; R_0 p = p","source_items":["S2.SS1.p1.4","S2.E4.m1","A1.Ex3.m2"],"semantics":"Piecewise zero-safe specular reflection; no continuity premise at a=0."},
 {"id":"flow","formula":"Φ_t(x,p) = (c+(cos t)•(x−c)+(sqrt η*sin t)•p, −(sin t/sqrt η)•(x−c)+(cos t)•p)","source_items":["A1.Ex2.m1","A1.Ex2.m2"],"semantics":"Finite real t only; η>0 fixes positive square root. No Φ_∞."},
 {"id":"bounce","formula":"S(x,p) = (x,R_(h(xRef,x)) p)","source_items":["A1.Ex3.m1","A1.Ex3.m2"],"semantics":"Position unchanged; actual zero-safe bounce. Borel is required internally; continuous S is unavailable."},
 {"id":"rate","formula":"λ(x,p) = sqrt η * max(0, inner p (h(xRef,x)))","source_items":["A1.Ex1.m1","S3.E9.m1"],"semantics":"Nonnegative actual PBPS rate, not a supplied bounded rate or generic hazard."},
 {"id":"energy","formula":"H(x,p) = (η⁻¹ * ‖x−c‖² + ‖p‖²)/2; E0 = H(z0)","source_items":["A1.Ex4.m1","A1.SS1.p3.m1"],"semantics":"Weighted SUM of position and momentum energies. E0 is exactly the original phase energy, not a caller-provided envelope."},
 {"id":"cap","formula":"C0 = sqrt η * β * sqrt(2*E0) * (sqrt(2*η*E0) + ‖c−xRef‖)","source_items":["A1.Ex6.m1"],"semantics":"Same original E0 for every active produced state and outgoing finite arc; C0≥0 may equal zero."},
 {"id":"integrated_hazard","formula":"Λ(z,u) = ∫ s in 0..u, λ(Φ_s(z))","source_items":["A1.E1.m2","A1.Ex7.m1"],"semantics":"u:NNReal, finite real-time integral. Continuous and nondecreasing are producer facts, not public assumptions."},
 {"id":"first_clock","formula":"τ(z,e) = inf {u:NNReal | e ≤ Λ(z,u)} : WithTop NNReal","source_items":["A1.E1.m1","A1.E1.m2","A1.SS1.p2.2"],"semantics":"Closed ≥ hitting set; inf empty=∞. e=0 gives τ=0. No-hit positive threshold may give ∞. Finite endpoint equality and joint Borel must come from actual75, whose fresh independent source admission is pending."},
 {"id":"record","formula":"Record = Sum (NNReal × (E × E)) Unit; time(inl(T,z))=↑T; time(inr())=∞","source_items":["A1.E2.m2","A1.SS1.p2.2"],"semantics":"Honest total representation of finite active postjump records and stopped marker. Stopped has no phase; no phase at∞ and no hidden arbitrary-state fallback."},
 {"id":"update","formula":"step(inr(),e)=inr(); step(inl(T,z),e)=inr() if τ(z,e)=∞, else inl(T+s, S(Φ_s(z))) for τ(z,e)=↑s","source_items":["A1.E2.m2","A1.SS1.p2.2"],"semantics":"Extract finite s only after guard. e=0 performs the literal zero-time S bounce and may repeat T. Marker absorption is total bookkeeping after source stop."},
 {"id":"finite_history","formula":"r_0=inl(0,z0); r_(n+1)=step(r_n,e_n), with e_n = source E_(n+1)","source_items":["A1.SS1.p2.m3","A1.SS1.p2.m4","A1.E1.m2","A1.E2.m2"],"semantics":"Each finite n depends only on threshold prefix e_0,…,e_(n−1). For deterministic e:Nat→NNReal this is an explicitly labelled extension of the source positive-iid construction, not an all-time physical path."},
 {"id":"outgoing_arc","formula":"arc_n(t)=Φ_t(z_n) when r_n=inl(T_n,z_n), 0≤t<τ(z_n,e_n)","source_items":["A1.SS1.p2.m7","A1.SS1.p2.m8"],"semantics":"A local finite-time arc only. Claim ζ_(T_n+t)=arc_n(t) as a single physical process requires later nonaccumulation/strict-positive clocks and stitching."}]
bridges=[
 ("B01","Derivative/Lipschitz regularity","hV and hH yield continuous gradient and β-Lipschitz residual; never add them as public binders.",["N01","N03"],"N06"),
 ("B02","Joint harmonic continuity","The literal flow is jointly continuous in y,xRef,z and finite t for fixed V,η.",["N03","N04"],"N09"),
 ("B03","Zero-safe bounce Borel","Split residual=0 and ≠0; singleton zero set is Borel, quotient formula continuous away from zero. Do not require global continuous S.",["N03","N21","N05"],"N09"),
 ("B04","Actual75 hazard/clock interface","Joint Borel actual τ, endpoint equality, e=0 and no-hit/top facts are reused only at their exact source boundary; compilation and independent math accepted per parent, fresh anti-source pending.",["N04","N06","N07"],"N09"),
 ("B05","Finite/top guard and extraction","{τ=∞} is Borel; on its complement extract finite s measurably. Never evaluate Φ or phase at∞.",["N07"],"N08"),
 ("B06","Stopped Sum step Borel","Disjoint sum branches and guarded composition give a joint Borel total one-step update; stop branch stores no phase.",["N08","N09"],"N10"),
 ("B07","Finite-index measurable induction","Evaluation e↦e_n is measurable in the product sigma algebra; base and recursively composed step give joint Borel finite r_n.",["N02","N09"],"N10"),
 ("B08","Active-state energy induction","Base H(z0)=E0, finite update uses exact flow and bounce preservation. Stop branch has no H to assert.",["N10","N11","N12"],"N13"),
 ("B09","Same-energy outgoing arc","Every finite Φ_t(z_n) from an active record has H=E0, including an infinite outgoing waiting interval.",["N12","N13"],"N14"),
 ("B10","Same-original uniform envelope","Apply E0 radii, β-Lipschitz gradient and Cauchy–Schwarz to actual rate; integrate to Λ(z_n,u)≤C0*u. No independent cap/provider premise.",["N01","N13","N14"],"N20"),
 ("B11","Extended deterministic waiting bound","For C0>0 obtain ↑(e_n/C0)≤τ in WithTop NNReal, including τ=∞ and e_n=0; for C0=0 positive threshold gives τ=∞, while e_n=0 still gives τ=0.",["N07","N14"],"N20"),
 ("B12","Inactive/absorbing semantics","Stopped marker propagates to every later finite index; active times are finite. No theorem about a stopped phase, physical all-time phase, or strictly increasing deterministic times.",["N08","N10"],"N10"),
 ("B13","Exact index and original data dependence","Threshold e_n is E_(n+1); same y,xRef,z0,V,η used at every step, finite-prefix dependence and actual E0 remain explicit.",["N02","N07","N08"],"N10")]
graph=json.loads(json.dumps(plan["source-proof-graph.json"]))
graph["schema"]="independent-source-first76-graph-v1"
graph["source_vs_Lean"]="All edges are source-proof ingredients or explicitly prospective internal bridges. This topology is not Lean implication and grants no formal result."
for n in graph["nodes"]:
    n["source_status_at_freeze"] = n.pop("status",None)
    n["status"]="SOURCE_OR_PROSPECTIVE_DEPENDENCY_ONLY"
    if n["id"]=="N07": n["parent75_boundary"]="Current compiled fd93d01583eec206285573c1f1631b94739f95471c50e1ff940e66080238e23d with independent math accepted per parent task; fresh anti-anchored source admission pending. No source-admitted claim."
    if n["id"]=="N16":
        n["meaning"]="Future iid exponential partial-sum divergence and its nonaccumulation consumer; deterministic single waiting increment split to N20."
        n["source_items"]=["A1.Ex9.m1","A1.SS1.p3.6","A1.SS1.p3.7"]
        n["status"]="DEFERRED_IID_SLLN_NOT_SELECTED"
graph["nodes"].extend([
 {"id":"N20","meaning":"Same-original-energy uniform extended waiting increment; positive-cap Ex8 and zero-cap/zero-threshold cases separated.","source_items":["A1.SS1.p3.5","A1.SS1.p3.m5","A1.Ex8.m1"],"status":"SELECTED_DETERMINISTIC_CONSUMER","public_extra_binder":False},
 {"id":"N21","meaning":"Literal source reflection R_a and explicit R0=I used in actual bounce.","source_items":["S2.SS1.p1.4","S2.SS1.p1.m8","S2.E4.m1"],"status":"SOURCE_LITERAL_DEFINITION","public_extra_binder":False}])
for e in graph["edges"]:
    if e["id"] in ["E25","E26"]:
        # Source-only correction: these ingredients produce Ex8, not iid/SLLN by themselves.
        for k in ["to","target","consumer"]:
            if k in e: e[k]="N20"
def edge(frm,to,reason):
    graph["edges"].append({"id":"E%02d"%(len(graph["edges"])+1),"producer":frm,"consumer":to,"meaning":reason,"truth":"source-ingredient-or-prospective-internal-bridge-not-Lean"})
edge("N20","N16","Deterministic increment would feed future iid partial-sum lower bound, not prove it now.")
edge("N21","N05","Literal reflection instantiates the zero-safe actual bounce.")
for ident,title,meaning,parents,target in bridges:
    graph["nodes"].append({"id":ident,"meaning":title+": "+meaning,"source_items":[],"status":"PROSPECTIVE_INTERNAL_PROOF_INGREDIENT","public_extra_binder":False})
    for p in parents: edge(p,ident,"Ingredient of "+ident)
    if ident!="B12": edge(ident,target,"Required internal producer for "+target)
graph["selected_nodes"]=["N08","N09","N10","N13","N20"]
graph["counts"]={"nodes":len(graph["nodes"]),"edges":len(graph["edges"]),"internal_bridges":len(bridges),"source_nodes":21,"selected_conclusion_nodes":5}
graph["scope_refinements_from_preread76"]=["Split Ex8 deterministic waiting lower bound into N20; N16 retains future iid/SLLN only.","Expand literal R definition from S2.E4 and zero-safe context.","Retain bib.bib12 as excluded wrong-locator input and add actual A1-linked bib.bib16 as excluded bibliographic correction; no Davis theorem content inferred."]
ids={n["id"] for n in graph["nodes"]}
assert len(ids)==len(graph["nodes"])
assert len({e["id"] for e in graph["edges"]})==len(graph["edges"])
assert all(e["producer"] in ids and e["consumer"] in ids for e in graph["edges"])
adj={n:[] for n in ids}
for e in graph["edges"]: adj[e["producer"]].append(e["consumer"])
done=set(); visiting=set()
def acyclic(node):
    assert node not in visiting, "source graph cycle at "+node
    if node in done: return
    visiting.add(node)
    for child in adj[node]: acyclic(child)
    visiting.remove(node); done.add(node)
for ident in ids: acyclic(ident)
checks.update({"all_graph_endpoints_valid":True,"graph_is_acyclic":True,"Ex8_split_edges_correct":all(e["consumer"]=="N20" for e in graph["edges"] if e["id"] in ["E25","E26"])})

def item_nodes(ident):
    if ident.startswith("S1.") or ident.startswith("S2.SS2."): return ["N01"]
    if ident in ["S2.E7.m1","S2.E8.m1"]: return ["N19"]
    if ident.startswith("S2.SS1.") or ident=="S2.E4.m1": return ["N21"]
    if ident=="S3.E4.m1": return ["N03"]
    if ident.startswith("S3.Thm"): return ["N18"]
    if ident.startswith("bib."): return []
    if ident.startswith("alg1.l1") or ident.startswith("alg1.l4"): return ["N02"]
    if ident.startswith("alg1.l2"): return ["N19"]
    if ident.startswith("alg1.l3"): return ["N03"]
    if ident.startswith("alg1.l5") or ident=="S3.E8.m1": return ["N04"]
    if ident.startswith("alg1.l6") or ident=="S3.E9.m1": return ["N06"]
    if ident.startswith("alg1.l7"): return ["N05"]
    if ident.startswith("alg1.l8"): return ["N18"]
    if ident in ["A1.SS1.p1.1","A1.SS1.p1.m1"]: return ["N02","N03"]
    if ident.startswith("A1.Ex1"): return ["N06"]
    if ident=="A1.SS1.p1.2": return ["N04","N05"]
    if ident.startswith("A1.Ex2"): return ["N04"]
    if ident.startswith("A1.Ex3") or ident in ["A1.SS1.p1.3","A1.SS1.p1.m2"]: return ["N05","N21"]
    if ident=="A1.SS1.p2.1": return ["N02","N15"]
    if ident in ["A1.SS1.p2.m1","A1.SS1.p2.m2"]: return ["N15"]
    if ident in ["A1.SS1.p2.m3","A1.SS1.p2.m4"]: return ["N02"]
    if ident.startswith("A1.E1"): return ["N07"]
    if ident.startswith("A1.E2") or ident.startswith("A1.SS1.p2."): return ["N08","N10"]
    if ident in ["A1.SS1.p3.1","A1.Ex4.m1","A1.SS1.p3.m1"]: return ["N11"]
    if ident=="A1.SS1.p3.2": return ["N12","N13"]
    if ident.startswith("A1.Ex5") or ident.startswith("A1.Ex6") or ident.startswith("A1.Ex7") or ident in ["A1.SS1.p3.3","A1.SS1.p3.4","A1.SS1.p3.m2","A1.SS1.p3.m3","A1.SS1.p3.m4"]: return ["N14"]
    if ident in ["A1.SS1.p3.5","A1.SS1.p3.m5","A1.Ex8.m1"]: return ["N20"]
    if ident=="A1.Ex9.m1" or ident=="A1.SS1.p3.6": return ["N16"]
    if ident in ["A1.SS1.p3.7","A1.SS1.p3.m6"]: return ["N16","N17","N18"]
    raise AssertionError("unclassified source item: "+ident)
promoted={"A1.SS1.p3.5","A1.SS1.p3.m5","A1.Ex8.m1"}
items=[]
for original in oldinv["items"]+extras:
    item=json.loads(json.dumps(original)); ident=item["item"]
    item["preread76_classification"]=original["classification"] if ident not in {x["item"] for x in extras} else None
    if ident in promoted: item["classification"]="NODE"
    item["independent_primary_rendering"]=readable(primary[slice(*item["primary_RAW_range"])])
    item["source_graph_nodes"]=item_nodes(ident)
    item["public_binder_credit"]=False
    item["Lean_proof_credit"]=False
    if item["classification"]=="EXCLUDED":
        if ident=="bib.bib12": reason="Excluded locator error: this is CCS+22, not Davis1984. Preserved original raw input; no mathematical evidence. Correct A1 href is bib.bib16."
        elif ident=="bib.bib16": reason="Actual A1-linked Davis1984 bibliography only; no text of Davis Section2 inspected and no theorem inferred."
        elif "p2.m1" in ident or "p2.m2" in ident: reason="Deferred independent Exp(1) threshold law and positivity consumer; deterministic sequence extension uses no iid premise."
        elif ident in ["A1.SS1.p3.6","A1.Ex9.m1","A1.SS1.p3.7","A1.SS1.p3.m6"]: reason="Deferred iid/SLLN divergence, nonaccumulation, all-time physical process and Markov arguments; no selected conclusion credit."
        elif ident.startswith("S3.Thm") or ident.startswith("alg1.l8"): reason="Deferred full well-posedness/stationarity/returned half-turn output; selected finite records do not imply these."
        else: reason="Outer same-J/Gaussian conditional initialization only; not a parent assumption of fixed-reference finite recursion."
        item["independent_disposition"]="EXCLUDED_CONTEXT_NO_SELECTED_CREDIT"
    else:
        reason="Exact source ingredient or scoped source context for "+", ".join(item["source_graph_nodes"])+"; supplied internally, never a new public premise."
        item["independent_disposition"]="SELECTED_SOURCE_INGREDIENT_OR_SCOPED_CONTEXT"
        if ident=="S1.p1.m1": reason="Target-density context only. No normalized target measure, partition function, initial law or moment input is needed for finite deterministic histories."
        if ident=="S1.E1.m1": reason="Original Hessian bounds supply hH. Display also defines κ=β/α, which is contextual and does not enter the selected conclusions/constants."
        if ident in ["alg1.l5","alg1.l5.m2"]: reason="Flow identity is selected; fixed algorithm horizon π is contextual only, and no return-at-π or process law is claimed."
        if ident=="A1.SS1.p2.1": reason="Mixed paragraph: select original phase/T0, exclude independent Exp(1) construction as individually classified mathematical subitems."
        if ident in ["A1.SS1.p2.2","A1.SS1.p2.m7","A1.SS1.p2.m8"]: reason="Select finite/top branch and outgoing local arcs. Physical ζ_(Tn+t) stitching is deferred for arbitrary-zero deterministic extension."
        if ident=="A1.SS1.p3.2": reason="Select H=H(z0) on produced active states and their finite arcs. Stop marker has no phase or energy."
        if ident=="A1.SS1.p3.3": reason="β-Lipschitz gradient is an internal consequence of original hV/hH, not a seventh caller; cap on local produced arcs selected, global path deferred."
        if ident in promoted: reason="New deterministic Ex8 scope selected; C0>0 extended bound includes top and e=0. Source no-jumps at C0=0 relies on positive exponential thresholds: for deterministic e=0 retain τ=0/instantaneous S update; for e>0 prove τ=∞."
        if ident=="A1.SS1.p1.3": reason="Source involution/vanishing rate and possible S discontinuity retained. No h=0 exclusion or global-continuity premise is legal. Zero-threshold extension may still apply S instantaneously."
    item["independent_reason"]=reason
    item["classification_delta_from_preread76"]={"from":"EXCLUDED","to":"NODE","reason":"Parent's new76 scope explicitly selects deterministic uniform waiting increment; iid/SLLN remains excluded."} if ident in promoted else None
    items.append(item)
coverage={"schema":"independent-source-first76-exhaustive-inventory-v1","scope":"Bounded source boundary only, before candidate76 header/body.","counts":{"items":len(items),"math_items":sum(x["formula_alttext"] is not None for x in items),"NODE":sum(x["classification"]=="NODE" for x in items),"EXCLUDED":sum(x["classification"]=="EXCLUDED" for x in items),"regions":len(regions)+len(newregions),"classification_promotions":len(promoted)},"items":items,"original_region_partition_count":partition_count,"original_literal_rendering_differences":literal_diffs,"new_regions":newregions,"classification_credit":"NODE is source coverage only: no theorem proved, source-reviewed, admitted or VERIFIED. Context-only restrictions are mandatory."}
formula_blocks=[]
for x in items:
    if x["formula_alttext"] is not None:
        a,b=x["primary_RAW_range"]
        formula_blocks.append({"item":x["item"],"formula_alttext":x["formula_alttext"],"primary_RAW_range":[a,b],"classification":x["classification"],"source_graph_nodes":x["source_graph_nodes"],**rawpin(primary[a:b])})

future={"iid_thresholds":"Future canonical Ω=Nat→Real with product Exp(1) law and e_n=(ω_n).toNNReal; positivity, unit mean/integrability, independence and SLLN must be derived, never added to original six source callers.","C0_zero":"Handle C0=0 separately; positive thresholds stop immediately. For arbitrary deterministic zeros, zero-time records can recur.","finite_growth":"For C0>0 and active predecessors, future sum of deterministic bounds yields source Ex9 lower bound. Divergence/a.s. nonaccumulation needs iid/SLLN consumer not selected now.","global_path":"Unique all-time physical phase requires positive clocks/nonaccumulation and stitching; no ζ∞ and no physical phase asserted for arbitrary zeros.","not_accepted":["nonexplosion","time-homogeneous Markov property","stationarity/invariance","conditional half-turn kernel","returned xπ","main theorem","error bounds","expected-query costs","actual-input composition","full paper exposition","post-merge PURIFIED","live delivery","Goal completion"]}
boundary={"schema":"independent-source-first76-boundary-v1","reviewer_role":"Independent prospective source/header reviewer, source-only stage.","parent_task":"/root/independent_source75","owned_write_directory":str(OWN.relative_to(ROOT)).replace("\\","/"),"no_candidate76_read":True,"no_review_decisions_read_for76":True,"original_six_callers":callers,"typing_classes":typing,"data_quantifiers":{"fixed_analytic_data":"E,V,α,β,η with original six callers and five typing classes","joint_variables":"y,xRef:E; z0:E×E; e:Nat→NNReal; n:Nat","arc_variable":"t:NNReal or finite real t with t≥0; outgoing arc interpretation restricted to 0≤t<τ","legal_degenerate_cases":["rank(E)=0","α*η=1","H(z0)=0","C0=0","e_n=0","τ=∞"]},"actual_literal_definitions":definitions,"selected_conclusions":["Exact guarded active/stopped one-step law and absorbing stop marker.","Exact finite recursion base and source threshold shift e_n=E_(n+1).","Joint Borel dependence of each finite record and event-time projection, with phase only in active branch.","H(z_n)=H(z0) for every produced active finite record and every finite outgoing flow arc.","Same C0 based on H(z0) bounds actual outgoing rates and integrated hazards.","For C0>0, ↑(e_n/C0)≤τ(z_n,e_n), including top and zero; corresponding active next-event-time increment. For C0=0 and e_n>0, τ=∞. For e_n=0, τ=0 even if C0=0."],"internal_proof_ingredients":[{"id":b[0],"title":b[1],"requirement":b[2],"public_extra_binder":False} for b in bridges],"future_consumer":future,"forbidden_extra_callers":["arbitrary flow/bounce/rate/clock provider","separate Lipschitz-gradient premise","global continuous bounce premise","arbitrary invariant family or cap","nonexplosion","iid/positive-all-thresholds premise for deterministic result","unbounded integrated hazard or a.s. finite waiting time","arbitrary stopped phase/default phase","extra derivative regularity"],"parent75_current_boundary":"Per parent task only: actual75 module compiled at fd93d01583eec206285573c1f1631b94739f95471c50e1ff940e66080238e23d; independent mathematical review accepted; fresh anti-anchored source review pending. This stage does not read module75 or grant its source admission.","plan_corrections":[{"kind":"scope_split","description":"Ex8 deterministic increment selected separately from future Ex9 iid/SLLN.","public_binder_change":False},{"kind":"bibliographic_locator","description":"Original Davis12-bibliographic snapshot is bib.bib12 CCS+22. Actual A1 citation href targets bib.bib16 Davis1984, bound separately as excluded bibliography only.","public_binder_change":False}],"claims_not_made":future["not_accepted"]}
pins={}
pins["graph"]=write("source-proof-graph76.json",graph)
pins["coverage"]=write("source-coverage-inventory76.json",coverage)
pins["formulas"]=write("exact-source-formulas76.json",{"schema":"independent-source-first76-exact-formulas-v1","count":len(formula_blocks),"blocks":formula_blocks,"literal_definition_semantics":definitions})
pins["boundary"]=write("source-boundary76.json",boundary)
pins["inputs"]=write("source-first76.input-manifest.json",{"schema":"independent-source-first76-input-manifest-v1","read_boundary":"Fixed primary and exactly five source-only plan JSONs plus their nine exact source-region snapshots. No candidate76 header/Lean or prior review decisions.","inputs":inputs,"derived_exact_primary_regions":newregions,"input_count":len(inputs),"primary_pin":rawpin(primary)})
checks.update({"all_94_items_raw_exact":len(items)==94,"all_58_math_alttexts_exact":len(formula_blocks)==58,"all_items_explicitly_disposed":all(x["independent_reason"] for x in items),"all_NODE_items_mapped":all(x["source_graph_nodes"] for x in items if x["classification"]=="NODE"),"six_callers_five_typing":len(callers)==6 and len(typing)==5,"thirteen_internal_bridges":len(bridges)==13,"no_candidate_or_review_decision_read":True})
assert all(checks.values()), checks
assert not literal_diffs, literal_diffs
pins["validation"]=write("source-first76.validation.json",{"schema":"independent-source-first76-validation-v1","status":"PASS_SOURCE_ONLY_FREEZE","checks":checks,"counts":coverage["counts"],"graph_counts":graph["counts"],"literal_rendering_difference_count":len(literal_diffs),"writer_pid":os.getpid(),"process_exit_expected":0,"not_compiler_or_source_admission":True})
freeze={"schema":"independent-source-first76-stageA-freeze-v1","stage":"SOURCE_ONLY_FROZEN_WAITING_FOR_CANDIDATE76_HEADER","created_UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"reviewer":"/root/independent_source75 acting as separate source76 prospective reviewer","frozen_before_any76_header_or_body":True,"prior76_review_decisions_visible":False,"source_pin":rawpin(primary),"artifacts":pins,"original_source_plan_preserved":True,"source_only_construction_diagnostics":"Superseded construction attempts retained in source-only-construction-attempt1/ and attempt2/. Corrected rendering/count and graph endpoint schema before parent notification; no source mathematical boundary changed and no candidate was read.","write_directory_remains_open":True,"no_CLOSED_or_VERIFIED_transition":True,"writer_pid":os.getpid(),"writer_exit_expected":0}
freeze_pin=write("stageA.freeze76.json",freeze)
print(json.dumps({"status":"PASS_SOURCE_ONLY_FREEZE","counts":coverage["counts"],"graph_counts":graph["counts"],"source_input_count":len(inputs),"partition_count":partition_count,"literal_differences":literal_diffs,"freeze":freeze_pin,"writer_pid":os.getpid(),"exit":0},ensure_ascii=False,sort_keys=True))
