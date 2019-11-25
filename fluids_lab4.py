import matplotlib.pyplot as plt

x = [0, 5.083, 10.17,15.25, 20.33, 25.42, 30.5]
h1 = [0.494, 0.478, 0.443, 0.343,0.405, 0.425, 0.434]
h2 = [0.514,0.506,0.488,0.440,0.470,0.481,0.484]
v1 = [0.631, 0.787,1.051,1.575,1.051, 0.787,0.631]
v2 = [0.437, 0.544 ,0.727,1.090,0.727,0.544,0.437]

e1 = []
e2 = []

for i in range(7):
    e1.append(h1[i] + v1[i]**2/(2*9.8))
    e2.append(h2[i] + v2[i]**2/(2*9.8))

plt.plot(x,h1, label = "HGL-full", marker= 'o')
plt.plot(x,h2, label = "HGL-half", marker= 'o')
plt.plot(x, e1, label = "EGL-full", marker= 'o')
plt.plot(x,e2, label = "EGL-half", marker= 'o')
plt.legend(loc="upper left")
plt.xlabel("X (cm)")
plt.ylabel("HGL and EGL (m)")
plt.title("HGL and EGL plots")

# because of viscous friction
plt.show()

# print(e1)
# print(e2)
