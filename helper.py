import itertools
from functools import reduce
import matplotlib.pyplot as plt
import numpy as np


def channelSplit(image):
    return np.dsplit(image, image.shape[-1])


def plot_img_array(img_array, ncol=3):
    nrow = len(img_array) // ncol

    f, plots = plt.subplots(nrow, ncol, sharex='all',
                            sharey='all', figsize=(ncol * 4, nrow * 4))

    for i in range(len(img_array)):
        plots[i // ncol, i % ncol]
        if (i % ncol == 0):
            [B, G, R] = channelSplit(img_array[i])
            im_ = plots[i // ncol, i % ncol].imshow(B, cmap='jet')
            # plt.colorbar(im_)
        else:
            plots[i // ncol, i % ncol].imshow(img_array[i])


def plot_side_by_side(img_arrays):
    flatten_list = reduce(lambda x, y: x+y, zip(*img_arrays))

    plot_img_array(np.asarray(flatten_list), ncol=len(img_arrays))


def plot_errors(results_dict, title):
    markers = itertools.cycle(('+', 'x', 'o'))

    plt.title('{}'.format(title))

    for label, result in sorted(results_dict.items()):
        plt.plot(result, marker=next(markers), label=label)
        plt.ylabel('dice_coef')
        plt.xlabel('epoch')
        plt.legend(loc=3, bbox_to_anchor=(1, 0))

    plt.show()


def masks_to_colorimg(masks):
    # colors = np.asarray([(201, 58, 64), (242, 207, 1), (0, 152, 75), (101, 172, 228),(56, 34, 132), (160, 194, 56)])
    # colors = np.asarray([(201, 58, 64), (242, 207, 1)])
    colors = np.asarray([(83, 191, 157), (255, 197, 77)])

    colorimg = np.ones(
        (masks.shape[1], masks.shape[2], 3), dtype=np.float32) * 255
    channels, height, width = masks.shape

    for y in range(height):
        for x in range(width):
            selected_colors = colors[masks[:, y, x] < 0.5]

            if len(selected_colors) > 0:
                colorimg[y, x, :] = np.mean(selected_colors, axis=0)

    return colorimg.astype(np.uint8)
