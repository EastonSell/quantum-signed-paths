"""Fixed random-bit budget, exponential reference probability oracle by default."""
import base_quantum as q

def rank_sample(x, gates, rank, oracle=q.probability):
    q.validate(x,gates)
    total=1 << sum(g[0]=='H' for g in gates)
    if type(rank) is not int or not 0<=rank<total:
        raise ValueError('rank must be an integer in [0, 2^h)')
    prefix=(); mass=total; calls=0
    for _ in x:
        left=oracle(x,gates,prefix+(0,))*total; calls+=1
        if left.denominator!=1 or not 0<=left<=mass:
            raise ValueError('oracle violates integer prefix mass invariant')
        left=int(left)
        if rank<left:
            prefix+=(0,); mass=left
        else:
            prefix+=(1,); rank-=left; mass-=left
    return prefix,calls

def bit_sample(x, gates, fair_bit):
    q.validate(x,gates)
    rank=0
    for _ in range(sum(g[0]=='H' for g in gates)):
        bit=fair_bit()
        if type(bit) is not int or bit not in (0,1):
            raise ValueError('fair_bit must return integer zero or one')
        rank=2*rank+bit
    return rank_sample(x,gates,rank)
