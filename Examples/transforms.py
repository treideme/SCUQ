import scuq.units as units
import scuq.si as si

# Defining Fahrenheit
fahrenheit = si.CELSIUS * 9.0 / 5.0 + 32
print fahrenheit

# Celsius to Fahrenheit
far_cel = si.CELSIUS.get_operator_to(fahrenheit)
print far_cel.convert(238)                       # ~100 °C

# Fahrenheit to Celsius
cel_far = fahrenheit.get_operator_to(si.CELSIUS)
print cel_far.convert(100)                       # ~238 °F

# The Operators can also be inverted using "~"
print (~far_cel).convert(100)                    # ~238 °F
print (~cel_far).convert(238)                    # ~100 °C

# ... and chained using *
print (cel_far * far_cel).convert(238)           # 238 °F
