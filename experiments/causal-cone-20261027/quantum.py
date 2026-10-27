"""Exponential reference algorithms; standard library only; wire zero is MSB."""
from fractions import Fraction
from itertools import product


def validate(x, gates, prefix=()):
    if any(b not in (0, 1) for b in (*x, *prefix)) or len(prefix)>len(x):
        raise ValueError('basis bits and prefix must be binary and dimension-compatible')
    for g in gates:
        if not g or g[0] not in ('H','T') or len(g)!={'H':2,'T':4}[g[0]]:
            raise ValueError('expected H(wire) or T(control,control,target)')
        if len(set(g[1:]))!=len(g)-1 or any(type(i) is not int or not 0<=i<len(x) for i in g[1:]):
            raise ValueError('distinct valid wire indices required')


def paths(x, gates):
    """Enumerate all h branch bits and their final basis string/sign parity."""
    validate(x,gates)
    h=sum(g[0]=='H' for g in gates)
    for choices in product((0,1),repeat=h):
        wire=list(x); parity=0; j=0
        for g in gates:
            if g[0]=='H':
                i=g[1]; b=choices[j]; j+=1
                parity ^= wire[i]&b; wire[i]=b
            else:
                _,a,b,t=g; wire[t]^=wire[a]&wire[b]
        yield tuple(wire),parity


def pair_counts(x,gates,prefix):
    validate(x,gates,prefix)
    p=list(paths(x,gates)); counts=[0,0]
    for a,s in p:
        if a[:len(prefix)]!=tuple(prefix): continue
        for b,t in p:
            if a==b: counts[s^t]+=1
    return counts[0],counts[1],2**sum(g[0]=='H' for g in gates)


def probability(x,gates,prefix):
    positive,negative,denominator=pair_counts(x,gates,prefix)
    return Fraction(positive-negative,denominator)


class CNF:
    """Width <=3 definitional encoding; exact exponential DPLL reference counter."""
    def __init__(self): self.n=0; self.clauses=[]
    def var(self): self.n+=1; return self.n
    def pin(self,v,b): self.clauses.append((v if b else -v,))
    def const(self,b):
        v=self.var(); self.pin(v,b); return v
    def conjunction(self,a,b):
        z=self.var(); self.clauses.extend([(-z,a),(-z,b),(z,-a,-b)]); return z
    def xor(self,a,b):
        z=self.var(); self.clauses.extend([(a,b,-z),(a,-b,z),(-a,b,z),(-a,-b,-z)]); return z
    def equal(self,a,b): self.clauses.extend([(-a,b),(a,-b)])
    def count(self):
        def recurse(clauses,free):
            while True:
                if any(not c for c in clauses): return 0
                if not clauses: return 1<<len(free)
                unit=next((c[0] for c in clauses if len(c)==1),None)
                if unit is None: break
                free=free-{abs(unit)}
                clauses=[tuple(v for v in c if v!=-unit) for c in clauses if unit not in c]
            v=min(clauses,key=len)[0]
            return sum(recurse(clauses+[(s,)],free) for s in (v,-v))
        return recurse(self.clauses,set(range(1,self.n+1)))
    def dimacs(self):
        return f'p cnf {self.n} {len(self.clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in self.clauses)


def encode(x,gates,prefix,parity):
    """Two copies; untouched fixed wires eliminated BEFORE variable allocation."""
    validate(x,gates,prefix)
    if parity not in (0,1): raise ValueError('parity must be binary')
    c=CNF(); active=sorted({i for g in gates for i in g[1:]})
    if any(i not in active and b!=x[i] for i,b in enumerate(prefix)):
        c.clauses.append(())
    finals=[]; signs=[]
    for copy in range(2):
        wire={i:c.const(x[i]) for i in active}; sign=c.const(0)
        for g in gates:
            if g[0]=='H':
                i=g[1]; choice=c.var()
                sign=c.xor(sign,c.conjunction(wire[i],choice)); wire[i]=choice
            else:
                _,a,b,t=g; wire[t]=c.xor(wire[t],c.conjunction(wire[a],wire[b]))
        finals.append(wire); signs.append(sign)
    for i in active:
        c.equal(finals[0][i],finals[1][i])
        if i<len(prefix): c.pin(finals[0][i],prefix[i])
    c.pin(c.xor(*signs),parity)
    return c


def state_probabilities(x,gates):
    """Independent dense state-vector: amplitudes a+b sqrt(2), rational a,b.

    Does not call path enumeration or CNF. Direct H butterflies and Toffoli
    permutation provide an exact, independently structured arithmetic oracle.
    """
    validate(x,gates)
    n=len(x); size=1<<n; state=[(Fraction(0),Fraction(0)) for _ in range(size)]
    idx=sum(bit<<(n-1-i) for i,bit in enumerate(x)); state[idx]=(Fraction(1),Fraction(0))
    for gate in gates:
        if gate[0]=='H':
            mask=1<<(n-1-gate[1]); new=list(state)
            for i in range(size):
                if i&mask: continue
                a,b=state[i]; c,d=state[i|mask]
                new[i]=(b+d,(a+c)/2); new[i|mask]=(b-d,(a-c)/2)
            state=new
        else:
            _,a,b,t=gate; ma=1<<(n-1-a); mb=1<<(n-1-b); mt=1<<(n-1-t)
            new=list(state)
            for i in range(size):
                j=i^mt if i&ma and i&mb else i
                new[j]=state[i]
            state=new
    out=[]
    for a,b in state:
        assert a*b==0, 'H/Toffoli homogeneous sqrt parity invariant'
        out.append(a*a+2*b*b)
    return out


def sample(x,gates,rng):
    """Sequential exact rational conditionals, finite integer random draws.

    randrange rejection draws have expected finite cost, not a fixed bit cap.
    """
    prefix=(); mass=Fraction(1)
    for _ in x:
        left=probability(x,gates,prefix+(0,)); ratio=left/mass
        bit=0 if rng.randrange(ratio.denominator)<ratio.numerator else 1
        prefix+=(bit,); mass=left if bit==0 else mass-left
        assert mass>0
    return prefix


def cone(x,gates,prefix):
    """Conservative backward support cone; prefix wires remain first after remap."""
    validate(x,gates,prefix)
    support=set(range(len(prefix))); kept=[]
    for gate in reversed(gates):
        wires=set(gate[1:])
        if support & wires:
            kept.append(gate); support.update(wires)
    ordered=sorted(support); remap={wire:i for i,wire in enumerate(ordered)}
    return tuple(x[i] for i in ordered), [tuple([g[0]]+[remap[i] for i in g[1:]]) for g in reversed(kept)]
