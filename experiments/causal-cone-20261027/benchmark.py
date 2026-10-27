"""Frozen exact comparison; standard-library only. Run from this directory."""
import json, random, time, tracemalloc, signal, platform, hashlib
from fractions import Fraction
from collections import defaultdict
from pathlib import Path
import quantum as q

def grouped(x,gates,prefix):
    sums=defaultdict(int)
    for y,s in q.paths(x,gates):
        if y[:len(prefix)]==tuple(prefix): sums[y]+=1 if s==0 else -1
    return Fraction(sum(v*v for v in sums.values()),1<<sum(g[0]=='H' for g in gates))

def dense(x,gates,prefix):
    values=q.state_probabilities(x,gates)
    target=sum(b<<(len(prefix)-1-i) for i,b in enumerate(prefix))
    return sum((v for i,v in enumerate(values) if i>>(len(x)-len(prefix))==target),Fraction(0))

def cases():
    for n in (3,5,8):
        for seed in range(4):
            for family in ('spectator','connected'):
                rng=random.Random(20261027+seed+100*n)
                x=tuple(rng.randrange(2) for _ in range(n))
                if family=='spectator':
                    gates=[('H',0),('T',0,1,2),('H',0)]+[('H',rng.randrange(1,n)) for _ in range(6)]
                else:
                    gates=[]
                    for _ in range(8):
                        gates += [('H',rng.randrange(n)),('T',*rng.sample(range(n),3))]
                for prefix in [(0,), (0,)*n]:
                    yield family,seed,x,gates,prefix

def timeout(signum,frame): raise TimeoutError('30-second per-call limit')

def main():
    out=Path('results'); out.mkdir(exist_ok=True)
    signal.signal(signal.SIGALRM,timeout)
    rows=[]
    methods={'pair':q.probability,'grouped':grouped,'dense':dense,
             'cone_grouped':lambda x,g,p:grouped(*q.cone(x,g,p),p),
             'cone_dense':lambda x,g,p:dense(*q.cone(x,g,p),p)}
    with (out/'benchmark.jsonl').open('w') as stream:
        for case_id,(family,seed,x,gates,prefix) in enumerate(cases()):
            xx,gg=q.cone(x,gates,prefix)
            h=sum(g[0]=='H' for g in gates); hc=sum(g[0]=='H' for g in gg)
            for name,fn in methods.items():
                reduced=name.startswith('cone_'); nn=len(xx) if reduced else len(x); hh=hc if reduced else h; gc=len(gg) if reduced else len(gates)
                row=dict(case_id=case_id,family=family,seed=seed,x=x,gates=gates,prefix=prefix,method=name,n=len(x),h=h,G=len(gates),cone_n=len(xx),cone_h=hc,cone_G=len(gg),
                    paths_enumerated=(1<<hh) if name!='dense' and name!='cone_dense' else None,
                    dense_state_slots=(1<<nn) if 'dense' in name else None,
                    dense_gate_slot_upper_bound=gc*(1<<nn) if 'dense' in name else None,
                    pair_comparison_upper_bound=(1<<(2*h)) if name=='pair' else None)
                try:
                    signal.alarm(30); start=time.perf_counter(); answer=fn(x,gates,prefix); elapsed=time.perf_counter()-start; signal.alarm(0)
                    row.update(probability=str(answer),seconds=elapsed)
                    tracemalloc.start(); signal.alarm(30); second=fn(x,gates,prefix); _,peak=tracemalloc.get_traced_memory(); signal.alarm(0); tracemalloc.stop()
                    row.update(python_peak_bytes=peak,status='ok' if second==answer else 'repeat_mismatch')
                except Exception as exc:
                    row.update(status=type(exc).__name__,error=str(exc))
                finally:
                    signal.alarm(0)
                    if tracemalloc.is_tracing(): tracemalloc.stop()
                rows.append(row); stream.write(json.dumps(row)+'\n'); stream.flush()
    failures=[]
    for i in range(48):
        group=[r for r in rows if r['case_id']==i]
        if len(group)!=5 or any(r['status']!='ok' for r in group) or len({r.get('probability') for r in group})!=1: failures.append(group)
    summary=dict(attempts=len(rows),expected_attempts=240,cases=48,failed_cases=len(failures),successful_calls=sum(r['status']=='ok' for r in rows),python=platform.python_version(),platform=platform.platform(),protocol_sha256=hashlib.sha256(Path('PROTOCOL.md').read_bytes()).hexdigest(),memory='tracemalloc Python allocation peak; not RSS; separately measured from elapsed time',timing='single untraced run, memory second pass, not a statistical speed claim')
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n'); (out/'failures.json').write_text(json.dumps(failures,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
