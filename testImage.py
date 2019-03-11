

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

I = Image.open('a.png')
a = np.asarray(I)
plt.imshow(a)