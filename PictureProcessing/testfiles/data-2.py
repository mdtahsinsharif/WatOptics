import matplotlib.pyplot as plt

import triangle as tr

box = tr.get_data('double_hex3')
t = tr.triangulate(box, 'p')
print(box)
tr.compare(plt, box, t)
plt.show()


# v = ['a', 'b', 'c', 'd']

# i = 0
# while i in range(len(v)-1):
#     print(i)
#     print("[i, i+1]: ", i, i+1)
#     i = i+1
# print(i, i - (len(v)-1))
