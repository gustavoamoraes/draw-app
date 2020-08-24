from PIL import Image
import numpy as np

def CreateImage (pixels):
	array = np.array(pixels, dtype=np.uint8)
	new_image = Image.fromarray(array)
	new_image.save('image.png')