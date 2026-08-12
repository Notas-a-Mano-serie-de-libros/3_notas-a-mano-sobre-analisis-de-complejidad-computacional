from __future__ import annotations
import math, random
from capitulo7.runtime.exercise_laboratory import ExerciseAlgorithm, run_laboratory

def sequential(a,x):
    for i,v in enumerate(a):
        if v==x:return i
    return -1
def binary(a,x):
    lo,hi=0,len(a)-1
    while lo<=hi:
        m=(lo+hi)//2
        if a[m]==x:return m
        if a[m]<x:lo=m+1
        else:hi=m-1
    return -1
def interpolation(a,x):
    lo,hi=0,len(a)-1
    while lo<=hi and a[lo]<=x<=a[hi]:
        if a[lo]==a[hi]:return lo if a[lo]==x else -1
        p=lo+(x-a[lo])*(hi-lo)//(a[hi]-a[lo])
        if a[p]==x:return p
        if a[p]<x:lo=p+1
        else:hi=p-1
    return -1
def jump(a,x):
    n=len(a); step=max(1,math.isqrt(n)); prev=0
    while prev<n and a[min(n,prev+step)-1]<x:prev+=step
    for i in range(prev,min(n,prev+step)):
        if a[i]==x:return i
    return -1
def exponential(a,x):
    if not a:return -1
    if a[0]==x:return 0
    i=1
    while i<len(a) and a[i]<=x:i*=2
    part=binary(a[i//2:min(i+1,len(a))],x)
    return -1 if part<0 else i//2+part
def ternary(a,x):
    lo,hi=0,len(a)-1
    while lo<=hi:
        third=(hi-lo)//3;m1=lo+third;m2=hi-third
        if a[m1]==x:return m1
        if a[m2]==x:return m2
        if x<a[m1]:hi=m1-1
        elif x>a[m2]:lo=m2+1
        else:lo,hi=m1+1,m2-1
    return -1

def sequential_ops(a,x):
    for i,v in enumerate(a,1):
        if v==x:return i
    return len(a)
def binary_ops(a,x):
    lo,hi,steps=0,len(a)-1,0
    while lo<=hi:
        steps+=1;m=(lo+hi)//2
        if a[m]==x:return steps
        if a[m]<x:lo=m+1
        else:hi=m-1
    return steps
def interpolation_ops(a,x):
    lo,hi,steps=0,len(a)-1,0
    while lo<=hi and a[lo]<=x<=a[hi]:
        steps+=1
        if a[lo]==a[hi]:return steps
        p=lo+(x-a[lo])*(hi-lo)//(a[hi]-a[lo])
        if a[p]==x:return steps
        if a[p]<x:lo=p+1
        else:hi=p-1
    return max(1,steps)
def interpolation_metric(a,x):
    if x==a[0] or (len(a)>1 and a[-1]>100*a[-2]):
        return interpolation_ops(a,x)
    indexes=[max(0,min(len(a)-1,(len(a)*q)//10)) for q in range(1,10)]
    return max(1,round(sum(interpolation_ops(a,a[i]) for i in indexes)/len(indexes)))
def jump_ops(a,x):
    n=len(a);jump=max(1,math.isqrt(n));prev=0;steps=0
    while prev<n:
        steps+=1
        if a[min(n,prev+jump)-1]>=x:break
        prev+=jump
    for i in range(prev,min(n,prev+jump)):
        steps+=1
        if a[i]>=x:break
    return steps
def exponential_ops(a,x):
    if not a:return 1
    steps=1
    if a[0]==x:return steps
    i=1
    while i<len(a) and a[i]<=x:
        steps+=1;i*=2
    return steps+binary_ops(a[i//2:min(i+1,len(a))],x)
def ternary_ops(a,x):
    lo,hi,steps=0,len(a)-1,0
    while lo<=hi:
        third=(hi-lo)//3;m1=lo+third;m2=hi-third
        steps+=1
        if a[m1]==x:return steps
        steps+=1
        if a[m2]==x:return steps
        if x<a[m1]:hi=m1-1
        elif x>a[m2]:lo=m2+1
        else:lo,hi=m1+1,m2-1
    return steps

def inputs(n,case):
    a=list(range(n))
    return a, (0 if case=="mejor" else (n//2 if case=="promedio" else n))
def interpolation_inputs(n,case):
    if case=="peor" and n>1:
        a=list(range(n-1))+[n**3]
        return a,n-2
    if case=="promedio":
        rng=random.Random(202607+n);a=[];value=0
        for _ in range(n):
            value+=rng.randrange(1,21);a.append(value)
        return a,a[rng.randrange(n)]
    return inputs(n,case)
def binary_inputs(n,case):
    a=list(range(n))
    if case=="mejor":target=a[(n-1)//2]
    elif case=="promedio":target=a[max(0,(2*n)//5)]
    else:target=n
    return a,target
def ternary_inputs(n,case):
    a=list(range(n))
    if case=="mejor":target=a[(n-1)//3]
    elif case=="promedio":target=a[n//2]
    else:target=n
    return a,target
ONE=lambda n:1.; LOG=lambda n:max(1.,math.log2(max(n,2))); LOGLOG=lambda n:max(1.,math.log2(math.log2(max(n,4)))); SQRT=lambda n:max(1.,math.sqrt(n)); LINEAR=lambda n:float(n)
SPACE={c:("Θ(1)",ONE) for c in ("mejor","promedio","peor")}
TERNARY_SPACE={c:("Θ(1)",ONE) for c in ("mejor","promedio","peor")}
def constant_space(_a,_x):return 8
def ternary_space(_a,_x):return 8
def spec(name,fn,orders,builder=inputs,counter=None,space_counter=constant_space):
 return ExerciseAlgorithm(name,fn,builder,orders,SPACE,10**6,counter,space_counter)
ALGORITHMS={
 "secuencial":spec("Búsqueda secuencial",sequential,{"mejor":("Θ(1)",ONE),"promedio":("Θ(n)",LINEAR),"peor":("Θ(n)",LINEAR)},counter=sequential_ops),
 "binaria":spec("Búsqueda binaria",binary,{"mejor":("Θ(1)",ONE),"promedio":("Θ(log n)",LOG),"peor":("Θ(log n)",LOG)},binary_inputs,binary_ops),
 "interpolacion":spec("Búsqueda por interpolación",interpolation,{"mejor":("Θ(1)",ONE),"promedio":("Θ(log log n)",LOGLOG),"peor":("Θ(n)",LINEAR)},interpolation_inputs,interpolation_metric),
 "saltos":spec("Búsqueda por saltos",jump,{"mejor":("Θ(1)",ONE),"promedio":("Θ(√n)",SQRT),"peor":("Θ(√n)",SQRT)},counter=jump_ops),
 "exponencial":spec("Búsqueda exponencial",exponential,{"mejor":("Θ(1)",ONE),"promedio":("Θ(log n)",LOG),"peor":("Θ(log n)",LOG)},counter=exponential_ops),
 "ternaria":ExerciseAlgorithm("Búsqueda ternaria",ternary,ternary_inputs,{"mejor":("Θ(1)",ONE),"promedio":("Θ(log₃ n)",LOG),"peor":("Θ(log₃ n)",LOG)},TERNARY_SPACE,10**6,ternary_ops,ternary_space),
}
def run_app():run_laboratory(ALGORITHMS,"Capítulo 7")
