# You have to import this module to use si units.
from scuq import *

# You can create product units using other instances of
# units:
myUnit = si.KILOGRAM*si.METER/si.SECOND**2
# This creates a unit that has the same physical dimension
# as the unit Newton.

# kg*m*s^(-2)
print str(myUnit)

# Lets test if they are equal...
print "si.NEWTON == myUnit: "+str(si.NEWTON == myUnit)
# Unexpectedly this returns False, but why?
# si.Newton is an AlternateUnit, it could have been the case
# that myUnit has not the same purpose as si.NEWTON. 

# However ...
print "si.NEWTON.is_compatible(myUnit): "\
	+str(si.NEWTON.is_compatible(myUnit))
# They may have different purposes, but they describe the same
# physical dimension. Therefore, they are compatible. 

# That means that one could convert among them.
operator = si.NEWTON.get_operator_to(myUnit)
print "operator.convert(1) = "+str(operator.convert(1))
# ... In this case the operator returns the identical value 
# (as expected).

# You can also do the above thing with an other unit than a 
# base unit.
myUnit = si.NEWTON * si.METER

# N*m
print myUnit

# Lets test if they are equal...
print "myUnit == si.KILOGRAM*si.METER**2/si.SECOND**2: "+ \
	str(myUnit == si.KILOGRAM*si.METER**2/si.SECOND**2)
# Unexpectedly this returns False, but why?
# si.Newton is again an AlternateUnit.

# However ...
print "myUnit.isCompatible(si.KILOGRAM*si.METER**2/si.SECOND**2): "+ \
	str(myUnit.is_compatible(si.KILOGRAM*si.METER**2/si.SECOND**2))
# They may have different purposes, but they describe the same
# physical dimension. Therefore, they are compatible. 

# As expected...
operator = myUnit.get_operator_to(si.KILOGRAM*si.METER**2/si.SECOND**2)
print "operator.convert(1) = "+str(operator.convert(1))

# This is to show that our library always maintains the Canonical
# form of a product of units.
myNewton = si.KILOGRAM*si.METER/si.SECOND**2

# yields: kg*m*s^(-2)
print str(myNewton)

# now lets create a unit that is compatible to si.PASCAL
myPascal = myNewton / si.METER**2

# yields: kg*m^(-1)*s(-2)
print str(myPascal)

# what happens if...
tmp = myPascal / myNewton
print str(tmp)
# should print: m^(-2)

# another trick: 
tmp = myPascal / myPascal
print str(tmp)
assert(tmp == units.ONE)
#yields the neutral element
