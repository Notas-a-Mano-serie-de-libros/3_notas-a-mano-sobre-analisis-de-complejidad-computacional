from __future__ import annotations
import math, random
from capitulo8.runtime.exercise_laboratory import ExerciseAlgorithm, run_laboratory

def bubble(a,_):
 a=a.copy();n=len(a)
 for i in range(n):
  changed=False
  for j in range(0,n-i-1):
   if a[j]>a[j+1]:a[j],a[j+1]=a[j+1],a[j];changed=True
  if not changed:break
 return a
def selection(a,_):
 a=a.copy()
 for i in range(len(a)):
  m=min(range(i,len(a)),key=a.__getitem__);a[i],a[m]=a[m],a[i]
 return a
def insertion(a,_):
 a=a.copy()
 for i in range(1,len(a)):
  x=a[i];j=i-1
  while j>=0 and a[j]>x:a[j+1]=a[j];j-=1
  a[j+1]=x
 return a
def shell(a,_):
 a=a.copy();gap=len(a)//2
 while gap:
  for i in range(gap,len(a)):
   x=a[i];j=i
   while j>=gap and a[j-gap]>x:a[j]=a[j-gap];j-=gap
   a[j]=x
  gap//=2
 return a
def merge(a,_):
 if len(a)<=1:return a.copy()
 m=len(a)//2;left=merge(a[:m],None);right=merge(a[m:],None);out=[];i=j=0
 while i<len(left) and j<len(right):
  if left[i]<=right[j]:out.append(left[i]);i+=1
  else:out.append(right[j]);j+=1
 return out+left[i:]+right[j:]
def quick(a,_):
 if len(a)<=1:return a.copy()
 pivot=a[-1];left=[x for x in a[:-1] if x<=pivot];right=[x for x in a[:-1] if x>pivot]
 return quick(left,None)+[pivot]+quick(right,None)
def radix(a,_):
 out=a.copy();exp=1;maximum=max(out,default=0)
 while maximum//exp:
  buckets=[[] for _ in range(10)]
  for value in out:buckets[(value//exp)%10].append(value)
  out=[value for bucket in buckets for value in bucket];exp*=10
 return out
def inputs(n,case):
 if case=="mejor":a=list(range(n))
 elif case=="peor":a=list(range(n,0,-1))
 else:
  a=list(range(n));random.Random(202608+n).shuffle(a)
 return a,None
def _balanced_last_pivot(values):
 if not values:return []
 middle=len(values)//2
 return _balanced_last_pivot(values[:middle])+_balanced_last_pivot(values[middle+1:])+[values[middle]]
def quick_inputs(n,case):
 if case=="mejor":a=_balanced_last_pivot(list(range(n)))
 elif case=="peor":a=list(range(n))
 else:
  a=list(range(n));random.Random(202608+n).shuffle(a)
 return a,None

def bubble_ops(a,_):
 a=a.copy();steps=0
 for i in range(len(a)):
  changed=False
  for j in range(0,len(a)-i-1):
   steps+=1
   if a[j]>a[j+1]:a[j],a[j+1]=a[j+1],a[j];changed=True
  if not changed:break
 return max(1,steps)
def selection_ops(a,_):return max(1,len(a)*(len(a)-1)//2)
def insertion_ops(a,_):
 a=a.copy();steps=0
 for i in range(1,len(a)):
  x=a[i];j=i-1
  while j>=0:
   steps+=1
   if a[j]<=x:break
   a[j+1]=a[j];j-=1
  a[j+1]=x
 return max(1,steps)
def shell_ops(a,_):
 a=a.copy();steps=0;gap=len(a)//2
 while gap:
  for i in range(gap,len(a)):
   x=a[i];j=i
   while j>=gap:
    steps+=1
    if a[j-gap]<=x:break
    a[j]=a[j-gap];j-=gap
   a[j]=x
  gap//=2
 return max(1,steps)
def merge_ops(a,_):
 def count(values):
  if len(values)<=1:return values,0
  m=len(values)//2;left,c1=count(values[:m]);right,c2=count(values[m:]);out=[];i=j=0;steps=c1+c2
  while i<len(left) and j<len(right):
   steps+=1
   if left[i]<=right[j]:out.append(left[i]);i+=1
   else:out.append(right[j]);j+=1
  return out+left[i:]+right[j:],steps
 return max(1,count(a)[1])
def quick_ops(a,_):
 stack=[a];steps=0
 while stack:
  values=stack.pop()
  if len(values)<=1:continue
  pivot=values[-1];left=[];right=[]
  for value in values[:-1]:
   steps+=1
   (left if value<=pivot else right).append(value)
  stack.extend((left,right))
 return max(1,steps)
def radix_ops(a,_):
 digits=max(1,len(str(max(a,default=0))))
 return max(1,len(a)*digits)
def constant_space(_a,_):return 8
def linear_space(a,_):return max(8,8*len(a))
def quick_space(a,_):
 monotone=all(a[i]<=a[i+1] for i in range(len(a)-1))
 depth=len(a) if monotone else max(1,math.ceil(math.log2(max(len(a),1))))
 return max(8,depth*24)
def radix_space(a,_):return max(80,8*(len(a)+10))
ONE=lambda n:1.; LINEAR=lambda n:float(n); QUAD=lambda n:float(n)**2; NLOG=lambda n:max(1.,n*math.log2(max(n,2))); RADIX=lambda n:max(1.,n*len(str(max(0,n-1))))
SP1={c:("Θ(1)",ONE) for c in ("mejor","promedio","peor")}; SPL={c:("Θ(n)",LINEAR) for c in ("mejor","promedio","peor")}
def orders(best,avg,worst):return {"mejor":best,"promedio":avg,"peor":worst}
ALGORITHMS={
 "burbuja":ExerciseAlgorithm("Ordenamiento burbuja",bubble,inputs,orders(("Θ(n)",LINEAR),("Θ(n²)",QUAD),("Θ(n²)",QUAD)),SP1,500,bubble_ops,constant_space),
 "seleccion":ExerciseAlgorithm("Ordenamiento por selección",selection,inputs,orders(("Θ(n²)",QUAD),("Θ(n²)",QUAD),("Θ(n²)",QUAD)),SP1,500,selection_ops,constant_space),
 "insercion":ExerciseAlgorithm("Ordenamiento por inserción",insertion,inputs,orders(("Θ(n)",LINEAR),("Θ(n²)",QUAD),("Θ(n²)",QUAD)),SP1,1000,insertion_ops,constant_space),
 "shell":ExerciseAlgorithm("Shell Sort",shell,inputs,orders(("O(n log n)",NLOG),("O(n^(3/2))",lambda n:n**1.5),("O(n²)",QUAD)),SP1,10000,shell_ops,constant_space),
 "mezcla":ExerciseAlgorithm("Merge Sort",merge,inputs,orders(("Θ(n log n)",NLOG),("Θ(n log n)",NLOG),("Θ(n log n)",NLOG)),SPL,10000,merge_ops,linear_space),
 "rapido":ExerciseAlgorithm("Quick Sort",quick,quick_inputs,orders(("Θ(n log n)",NLOG),("Θ(n log n)",NLOG),("Θ(n²)",QUAD)),orders(("Θ(log n)",lambda n:math.log2(max(n,2))),("Θ(log n)",lambda n:math.log2(max(n,2))),("Θ(n)",LINEAR)),2000,quick_ops,quick_space),
 "radix":ExerciseAlgorithm("Radix Sort",radix,inputs,orders(("Θ(nk)",RADIX),("Θ(nk)",RADIX),("Θ(nk)",RADIX)),SPL,100000,radix_ops,radix_space),
}
def run_app():run_laboratory(ALGORITHMS,"Capítulo 8")
