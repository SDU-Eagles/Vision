import matplotlib.pyplot as plt
import numpy as np

area        = [0.36, 0.36, 0.64, 0.64, 0.68]
perimeter   = [0.36, 0.20, 0.40, 0.32, 0.33]

plt.scatter(area, perimeter, color=['red','green','blue', 'yellow', 'orange'])
plt.xlabel('Area')
plt.ylabel('Perimeter')
plt.show()
