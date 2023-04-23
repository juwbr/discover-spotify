import numpy as np
from matplotlib.pyplot import imread as plt_imread
from multiprocessing import Pool


def get_html_colors(ids, path='images/tracks/', avoid_gray=3.0):
    """Return the background and font color of the images in the given path.
    The colors are returned as a dictionary.
    It uses multiprocessing to speed up the process.
    """
    
    ret = {}
    files = [path + file + '.jpg' for file in ids]
    parameters = [(file, avoid_gray) for file in files]
    tmp = Pool().map(__get_background_and_font_color, parameters)
    ret = {ids[i]: tmp[i] for i in range(len(ids))}
    return ret


def __get_background_and_font_color(parameters):
    """ Return the background and font color of the given image."""
    img_path, avoid_gray = parameters
    img = plt_imread(img_path)
    avg_color = __get_cool_average_color(img, avoid_gray)
    background_color = f'rgb({avg_color[0]}, {avg_color[1]}, {avg_color[2]})'
    text_color = __get_text_color(avg_color / 255)
    return {'background_color': background_color, 'text_color': text_color}


def __get_text_color(bg_color):
    """ Return the color of the text that should be used on the given background color."""
    if np.mean(bg_color) > 0.5:
        return 'black'
    else:
        return 'white'
    

def __get_cool_average_color(img, avoid_gray):
    """ Return the average color of the given image.
    The average color is calculated by using the saturation of each pixel as a weight.

    """

    # 1. calculate the saturation of each pixel
    saturation = np.zeros(img.shape[0:2])
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            avg = np.mean(img[i, j])
            saturation[i, j] = abs(img[i, j, 0] - avg) + abs(img[i, j, 1] - avg) + abs(img[i, j, 2] - avg)
            saturation[i, j] **= avoid_gray
    
    # 2. create a 3D array to store the weight of each color
    weights = np.zeros((256, 256, 256))
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            weights[img[i, j, 0], img[i, j, 1], img[i, j, 2]] += saturation[i, j]

    # 3. pool the weights
    weights_pooled = np.zeros((64, 64, 64))
    for i in range(64):
        for j in range(64):
            for k in range(64):
                weights_pooled[i, j, k] = np.max(weights[i*4:(i+1)*4, j*4:(j+1)*4, k*4:(k+1)*4])
                
    # 4. find the color with the highest weight
    max_weight = 0
    avg_color = [0, 0, 0]
    for i in range(64):
        for j in range(64):
            for k in range(64):
                if weights_pooled[i, j, k] > max_weight:
                    max_weight = weights_pooled[i, j, k]
                    avg_color = [i*4, j*4, k*4]

    return np.array(avg_color)


if __name__ == '__main__':
    ids = ['your', 'IDs', 'here']
    tmp = get_html_colors(ids)
    from pprint import pprint
    pprint(tmp)