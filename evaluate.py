"""Run frozen correctness suite; never drops failed rows or silently retries."""
import hashlib,json,random,traceback
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import quantum as q

ROOT=Path(__file__).parent

def cases():
    alphabet=[('H',0),('H',1),('H',2),('T',0,1,2)]
    for length in range(4):
        for gates in product(alphabet,repeat=length):
            for x in product((0,1),repeat=3): yield 'exhaustive',x,gates
    rng=random.Random(20261027)
    for _ in range(100):
        n=rng.randint(1,5); length=rng.randint(0,8)
        x=tuple(rng.randrange(2) for _ in range(n)); gates=[]
        for _ in range(length):
            if n<3 or rng.random()<.6: gates.append(('H',rng.randrange(n)))
            else: gates.append(('T',*rng.sample(range(n),3)))
        yield 'random',x,gates

def main():
    expected=(ROOT/'protocol.sha256').read_text().split()[0]
    assert hashlib.sha256((ROOT/'PROTOCOL.md').read_bytes()).hexdigest()==expected
    output=ROOT/'results'; output.mkdir(exist_ok=True)
    summary=Counter(); failures=[]
    with (output/'exact.jsonl').open('w') as stream:
        for case_id,(suite,x,gates) in enumerate(cases()):
            try:
                state=q.state_probabilities(x,gates)
                oracle_error=None
            except Exception:
                oracle_error=traceback.format_exc()
            for k in range(len(x)+1):
                for prefix in product((0,1),repeat=k):
                    row=dict(case_id=case_id,suite=suite,x=x,gates=gates,prefix=prefix,denominator=2**sum(g[0]=='H' for g in gates))
                    summary['attempted']+=1; summary[suite+'_attempted']+=1
                    try:
                        if oracle_error: raise RuntimeError(oracle_error)
                        pos,neg,den=q.pair_counts(x,gates,prefix)
                        cnfs=[q.encode(x,gates,prefix,p) for p in (0,1)]
                        counts=[c.count() for c in cnfs]
                        oracle=sum((p for i,p in enumerate(state) if tuple((i>>(len(x)-1-j))&1 for j in range(k))==prefix),Fraction(0))
                        good=counts==[pos,neg] and Fraction(pos-neg,den)==oracle and all(len(cl)<=3 for c in cnfs for cl in c.clauses)
                        row.update(positive=pos,negative=neg,denominator=den,cnf_counts=counts,state_probability=str(oracle),variables=cnfs[0].n,clauses=len(cnfs[0].clauses),passed=good)
                    except Exception:
                        good=False; row.update(passed=False,error=traceback.format_exc())
                    summary['passed' if good else 'failed']+=1
                    if not good: failures.append(row)
                    stream.write(json.dumps(row,sort_keys=True)+'\n'); stream.flush()
    rng=random.Random(20261027); x=(0,0,0); gates=[('H',i) for i in range(3)]
    hist=Counter(''.join(map(str,q.sample(x,gates,rng))) for _ in range(4096))
    tv=sum(abs(Fraction(hist.get(''.join(map(str,b)),0),4096)-Fraction(1,8)) for b in product((0,1),repeat=3))/2
    sampling=dict(seed=20261027,shots=4096,histogram=dict(sorted(hist.items())),total_variation=str(tv),claim='finite PRNG demonstration only')
    (output/'sampling.json').write_text(json.dumps(sampling,indent=2)+'\n')
    (output/'failures.json').write_text(json.dumps(failures,indent=2)+'\n')
    (output/'summary.json').write_text(json.dumps(dict(summary),indent=2)+'\n')
    print(json.dumps(dict(summary),indent=2))
    # Counterexample: H on unmeasured wire, |00> input, first-bit prefix 0.
    paths=list(q.paths((0,0),[('H',1)]))
    wrong=sum((-1)**(s^t) for a,s in paths for b,t in paths if a[0]==b[0]==0)/2
    counter=dict(circuit=[['H',1]],input=[0,0],prefix=[0],correct='1',incorrect_prefix_only_matching=wrong)
    (output/'counterexample.json').write_text(json.dumps(counter,indent=2)+'\n')
    if failures: raise SystemExit(1)

if __name__=='__main__': main()
