import matplotlib.pyplot as plt
import numpy as np  
values = np.array([1, 2, 3, 4, 5])
plt.plot(values, values**3, label='y = x^3')
plt.title('line y = x^3')
plt.show()