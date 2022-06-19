import os
import random
import time

from PIL import Image
import numpy as np

if __name__ == '__main__':

    downscaling_constant = 32
    overlay_transparency = 64
    range_width = 40
    colour_range = 10
    min_distance = 15
    colors = []
    i = min_distance
    colours = []
    while i < (min_distance + range_width):
        colors.append(i)
        i = i + colour_range

    for c in colors:
        colours.append(c)
        colours.append(c * -1)

    picture_dimension = (256, 256)  # In the current implementation, these need to be square and divisible by the
    # downscaling constant

    if picture_dimension[0] != picture_dimension[1] or picture_dimension[0] % downscaling_constant != 0:
        print(
            "Warning, invalid dimension or downscaling constant selection, the behaviour will probably not be correct")

    # PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
    img = Image.new('RGB', picture_dimension, "black")  # create a new black image

    arr = np.array(img)
    arr2 = np.array(img)
    arr3 = np.array(img)
    arr_encode = np.resize(arr, (int(img.size[0] / downscaling_constant), int(img.size[1] / downscaling_constant)))

    # fill values in smaller array
    for i in range(arr_encode.shape[0]):
        for j in range(arr_encode.shape[1]):
            arr_encode[i, j] = random.choice(colours)  # get random colour from the colour range

    # fill values in array based on the smaller array
    for i in range(arr.shape[0]):  # for every col:
        for j in range(arr.shape[1]):  # For every row
            arr[i, j] = 127 + arr_encode[int(i / downscaling_constant), int(j / downscaling_constant)]
            arr2[i, j] = 127 - arr_encode[int(i / downscaling_constant), int(j / downscaling_constant)]
            arr3[i, j] = 127


    img_overlay = Image.fromarray(arr).convert("RGBA")

    img_overlay.putalpha(overlay_transparency)
    img_overlay_complement = Image.fromarray(arr2).convert("RGBA")
    img_overlay_complement.putalpha(overlay_transparency)
    img_overlay_default = Image.fromarray(arr3).convert("RGBA")
    img_overlay_default.putalpha(overlay_transparency)
    img_final = Image.open('rainbow.png')


    Image.alpha_composite(img_final, img_overlay_default).save('rainbow-1.png')
    Image.alpha_composite(img_final, img_overlay_complement).save('rainbow-2.png')
    Image.alpha_composite(img_final, img_overlay).save('rainbow-3.png')

    os.system('ffmpeg -y -framerate 120 -i rainbow-%d.png output.mp4 -loglevel warning')
    time.sleep(1)
    os.system('ffmpeg -y -stream_loop 600 -i output.mp4 -c copy long.mp4 -loglevel warning')

    os.system('ffmpeg -y -framerate 120 -i rainbow-1.png real.mp4 -loglevel warning')
    time.sleep(1)
    os.system('ffmpeg -y -stream_loop 360 -i real.mp4 -c copy long2.mp4 -loglevel warning')
    print("Finished generating video")

