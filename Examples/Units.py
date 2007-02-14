import scuq.units as units
import scuq.si as si

print si.METER                 # ... meter
assert(isinstance(si.METER, units.BaseUnit))

SQMETER = si.METER ** 2        # ... define square meter
print SQMETER                  # ... m^(2)
assert(isinstance(SQMETER, units.ProductUnit))

SQMETER2 = si.METER * si.METER # ... another way
print SQMETER2                 # ... m^(2)
assert(SQMETER2 == SQMETER)    # ... still square meter

CELSIUS = si.KELVIN + 273.15   # ... define celsius on kelvin
print CELSIUS                  # ... (K+273.15)
assert(isinstance(CELSIUS, units.TransformedUnit))
