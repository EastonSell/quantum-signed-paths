import json, random, time
from collections import Counter
from itertools import product
from pathlib import Path
import base_quantum as q
import bounded as b

def cases():
    alphabet=[('H',0),('H',1),('H',2),('T',0,1,2)]
    for length in range(4):
        for gates in product(alphabet,repeat=length):
            for x in product((0,1),repeat=3):
                yield 'exhaustive',x,gates
    rng=random.Random(20261027)
    for _ in range(40):
        n=rng.randint(1,4); length=rng.randint(0,6)
        x=tuple(rng.randrange(2) for _ in range(n)); gates=[]
        for _ in range(length):
            if rng.random()<0.6 or n<3: gates.append(('H',rng.randrange(n)))
            else: gates.append(('T',*rng.sample(range(n),3)))
        yield 'seeded',x,gates

def run(out):
    out.mkdir(parents=True,exist_ok=False)
    failures=[]; stats={}; start=time.perf_counter()
    with (out/'rows.jsonl').open('w') as f:
        for case_id,(group,x,gates) in enumerate(cases()):
            s=stats.setdefault(group,dict(cases=0,ranks=0,oracle_calls=0,failed_cases=0))
            s['cases']+=1
            try:
                h=sum(g[0]=='H' for g in gates); denominator=1<<h
                probabilities=q.state_probabilities(x,gates)
                masses=[p*denominator for p in probabilities]
                assert all(v.denominator==1 and v>=0 for v in masses)
                expected=[i for i,v in enumerate(masses) for _ in range(int(v))]
                assert len(expected)==denominator
                actual=[]; calls=[]
                for rank in range(denominator):
                    bits,count=b.rank_sample(x,gates,rank)
                    value=sum(v<<(len(x)-1-j) for j,v in enumerate(bits))
                    actual.append(value); calls.append(count)
                hist=Counter(actual)
                passed=(actual==expected and all(c==len(x) for c in calls) and all(hist[i]==v for i,v in enumerate(masses)))
                s['ranks']+=denominator; s['oracle_calls']+=sum(calls)
                row=dict(case_id=case_id,group=group,x=x,gates=gates,h=h,denominator=denominator,actual=actual,expected=expected,calls=calls,masses=list(map(int,masses)),passed=passed)
                if not passed: failures.append(row); s['failed_cases']+=1
            except Exception as exc:
                row=dict(case_id=case_id,group=group,x=x,gates=gates,error=repr(exc)); failures.append(row); s['failed_cases']+=1
            f.write(json.dumps(row)+'\n')
    summary=dict(groups=stats,failures=len(failures),elapsed_seconds=time.perf_counter()-start)
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (out/'failures.json').write_text(json.dumps(failures,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
    if failures: raise SystemExit(1)
if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True)
    run(Path(parser.parse_args().output))
