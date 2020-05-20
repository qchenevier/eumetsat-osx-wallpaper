import glob
import os
import requests

import numpy as np

#%%
def _rasterio_data_to_image(array):
    return array.swapaxes(0, 2).swapaxes(0, 1)

def download_image(image_url):
    from rasterio.io import MemoryFile
    response_image = requests.get(image_url, verify=False)
    with MemoryFile(response_image.content) as memfile:
        with memfile.open() as dataset:
            data_array = dataset.read()
    return _rasterio_data_to_image(data_array)

def open_image_file(image_file):
    from PIL import Image
    return np.array(Image.open(image_file))

def crop_bottom_of_image(image_array, n_pixels):
    return image_array[:-n_pixels, :, :]

def add_black_margin(image_array, n_pixels):
    pad_width = ((n_pixels, n_pixels), (n_pixels, n_pixels), (0, 0))
    return np.pad(image_array, pad_width, constant_values=0)

def color_mixing(image_array, mix=0.3):
    new_image_array = image_array.copy()
    genuine_norm = (new_image_array**2).sum(axis=2)

    red = new_image_array[:, :, 0]
    green = new_image_array[:, :, 1]
    blue = new_image_array[:, :, 2]

    new_image_array[:, :, 0] = (1-mix)*red + mix*green
    new_image_array[:, :, 1] = (1-1.5*mix)*green + mix*red + 0.5*mix*blue
    new_image_array[:, :, 2] = blue

    norm = (new_image_array**2).sum(axis=2)

    return np.nan_to_num(new_image_array * np.dstack(3*[genuine_norm]) / np.dstack(3*[norm]), 0).clip(max=1)

def saturate(x, factor=2):
    return np.tanh((x-0.5)*factor)/np.tanh(0.5*factor)/2 + 0.5

#%%
# https://github.com/domoritz/himawari-8-chrome/pull/29
response = requests.get("https://meteosat-url.appspot.com/msg", verify=False)

image_url = response.json()["url"]
image_date = (
    response.json()["date"]
    .replace(":", "-")
    .replace(" ", "_")
)

image_file = f"earth_{image_date}.png"

#%%
BOTTOM_CROP = 79
BLACK_MARGIN = 50
COLOR_MIXING = 0.3
SATURATION_FACTOR = 1.75

if not os.path.exists(image_file):

    mask_image_array = open_image_file("mask_raw.png")[:, :, :3]

    image_array = download_image(image_url)

    image_array = (image_array * (1 - mask_image_array / 255)).astype("uint8").clip(min=0) / 255
    image_array = crop_bottom_of_image(image_array, n_pixels=BOTTOM_CROP)
    image_array = add_black_margin(image_array, n_pixels=BLACK_MARGIN)

    image_array = color_mixing(image_array, mix=COLOR_MIXING)
    image_array = saturate(image_array, factor=SATURATION_FACTOR)

    image_array_int = (image_array * 255).astype(np.uint8)

    for f in glob.glob("earth*.png"):
        os.remove(f)

    from PIL import Image
    Image.fromarray(image_array_int).save(image_file)

dir_path = os.path.dirname(os.path.realpath(__file__))
change_desktop_shell_command = (
    f"""osascript -e 'tell application "System Events" """
    f"""to set picture of every desktop to POSIX file "{dir_path}/{image_file}"'"""
)
os.system(change_desktop_shell_command)
