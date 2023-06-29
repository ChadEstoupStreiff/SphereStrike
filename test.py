import math

u = (5, 6)
v = (2, 1)

v_m = math.sqrt(v[0] ** 2 + v[1] ** 2)
v_u = (v[0] / v_m, v[1] / v_m)
print(v_m)
print(v_u)

ps = u[0] * v_u[0] + u[1] * v_u[1]

print(ps)
proj_u = (ps * v_u[0], ps * v_u[1])

print(proj_u)