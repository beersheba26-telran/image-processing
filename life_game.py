import numpy as np
import matplotlib.pyplot as plt
from life_game_matrix import getInitialMatrix, getNextMatrix
SHAPE_0 = 20
SHAPE_1 = 20
LIMIT = 100
img: np = getInitialMatrix(SHAPE_0, SHAPE_1)
img_next: np = None
iteration: int = 0
prev_state_1 = None
prev_state_2 = None
plt.ion()
fig, ax = plt.subplots()
plot = ax.imshow(img, cmap="gray", vmin=0, vmax=1)

while iteration < LIMIT:
    img_next = getNextMatrix(img)
    if np.array_equal(img, img_next) or (
        prev_state_1 is not None and np.array_equal(prev_state_1, img_next)
    ) or (prev_state_2 is not None and np.array_equal(prev_state_2, img_next)):
        break

    prev_state_2 = prev_state_1
    prev_state_1 = img
    img = img_next
    plot.set_array(img)
    fig.canvas.draw()
    fig.canvas.flush_events()
    iteration += 1
    
print(f"Game ended after {iteration} iterations")    
plt.ioff()
plt.savefig("life_game.png") #saving final image state
plt.close()
