vmax = 1

v1 = 0.95
v2 = 0.75

vsum = v1 + v2

scale = vmax / vsum
print scale

v1 = scale * v1
v2 = scale * v2

vsum = v1 + v2
print v1
print v2
print vsum
