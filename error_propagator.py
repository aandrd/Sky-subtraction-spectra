# Alain Andrade - PhD(c) Universidad Andres Bello
from sympy import *
import numpy as np

# this script was made to estimate non-statiscal errors (insturmental) by using the derivative expresion
# so you need to put the variables (with the errors), and also specify the function that you need to propagate 



# algebraic variables –––––––––––––––––––––––––––––––––––––––––––––––––––––––––
var = symbols('M m')    #put variables
# a,b,c = symbols('a b c')    #put algebraic coefficent
err= symbols('s1 s2')   # errors of each variable repectively
f=10**((1/5)*(var[1]-var[0]+5))   #function that we want to propagate (in this case the distance of a source)

# eval ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
ev_var=[-2.34,16.71818] # values of the variables
ev_err=[0.007,0.01] # values of the errors

# cycle for doing the chain rule––––––––––––––––––––––––––––––––––––––––––––––––
arr=[]
for i in range(len(var)):
    prop=diff(f,var[i])*err[i]  #make derivative with error 
    arr.append(prop)
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
sigma= factor(sum(np.abs(np.array(arr))))   #make algebraic epression of absolute error
# sigma= factor(sqrt(sum(np.array(arr)**2)))  #make algebraic expression of STD
numeric= sigma.subs([(var[0],ev_var[0]),(var[1],ev_var[1]),(err[0],ev_err[0]),(err[1],ev_err[1])])

print(f'the analitic expression for propagation :')
pprint(sigma)
print(f'the uncertainly is : {numeric.evalf()}')