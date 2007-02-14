import scuq.units as units
import scuq.si as si

# Define the unit litre
litre = (si.METER ** 3)
litre = litre/1000.0

# Define the unit m^2 / l used for paint coverage
u_paint_coverage = units.AlternateUnit("pc", si.METER ** 2 
                                             / litre)

# Define the unit m^{-1}
u_inv_meter = ~si.METER

print (u_paint_coverage == u_inv_meter)              # False
print (u_paint_coverage.is_compatible(u_inv_meter))  # True
