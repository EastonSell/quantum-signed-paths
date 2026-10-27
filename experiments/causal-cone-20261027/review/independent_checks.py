import json,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import quantum as q
r=random.Random(99982); checked=0
for n in range(1,7):
 for _ in range(50):
  x=tuple(r.randrange(2) for j in range(n)); gates=[]
  for j in range(15):
   gates.append(('H',r.randrange(n)) if n<3 or r.random()<.6 else ('T',*r.sample(range(n),3)))
  k=r.randrange(n+1); p=tuple(r.randrange(2) for j in range(k)); xx,gg=q.cone(x,gates,p)
  def prob(xx,gg):
   v=q.state_probabilities(xx,gg); target=sum(b<<(k-j-1) for j,b in enumerate(p))
   return sum(a for i,a in enumerate(v) if i>>(len(xx)-k)==target)
  assert prob(x,gates)==prob(xx,gg),(x,gates,p)
  checked+=1
print('Independent longer/random cases:',checked)
a=[json.loads(s) for s in open(ROOT/'review/benchmark-rerun.jsonl')]; b=[json.loads(s) for s in open(ROOT/'results/benchmark.jsonl')]
ignore={'seconds','python_peak_bytes'}
assert [{k:v for k,v in row.items() if k not in ignore} for row in a]==[{k:v for k,v in row.items() if k not in ignore} for row in b]
print('All 240 rows match exactly excluding timings and memory')
