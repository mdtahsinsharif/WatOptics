import matplotlib.pyplot as plt

import triangle as tr

box = tr.get_data('double_hex3')
print(box)
t = tr.triangulate(box, 'p')
v = t['vertices'].tolist()
# print(box)
tList = t['triangles'].tolist()
tCoords = [] ## coordinates of the triangles: [[[0,0], [0,1], [1,0]], [...]]
for tL in tList:
        tCoords.append([v[tL[0]], v[tL[1]], v[tL[2]]])

print(tCoords)

tr.compare(plt, box, t)
plt.show()
