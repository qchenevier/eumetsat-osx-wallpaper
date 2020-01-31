import glob
import numpy as np
import rasterio
from matplotlib import image

#%%
files = list(glob.glob("sample_eumetsat_images/*.jpg"))

#%%
data_array = np.stack([rasterio.open(file).read() for file in files])
mask_data_array = data_array.min(axis=0)
mask_image_array = mask_data_array.swapaxes(0, 2).swapaxes(0, 1)
mask_image_array = ((mask_image_array > 50) * 255).astype("uint8")

mask_image_file = "mask_raw.png"
image.imsave(mask_image_file, mask_image_array)
