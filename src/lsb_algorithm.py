import cv2

from src import utility

import numpy as np
from matplotlib import pyplot as plt


def display_img(image):
    cv2.imshow('Cover Image', image)
    cv2.waitKey()
    cv2.destroyAllWindows()


def plot_histogram(path):
    img = cv2.imread(path, 0)
    plt.hist(img.ravel(), 256, [0, 256])
    plt.show()


class LSB:
    def __init__(self, data_path=None, image_path=None, save_path=None):
        self.data = data_path
        self.cover_img_path = image_path
        plot_histogram(self.cover_img_path)
        self.img = None
        self.save_dir = save_path
        self.image_type = None
        self.max_image_size = 0
        self.utils = utility.Utility(self.data)
        assert self.cover_img_path is not None
        self.file_type = self.data.split('.')[-1] if self.data else None
        self.prepare_img()

    def prepare_img(self):
        self.image_type = self.cover_img_path.split('.')[-1]
        if self.image_type.upper() == 'PNG':
            self.img = cv2.imread(self.cover_img_path)
            plt.hist(self.img.ravel(), 256, [0, 256])
            plt.show()
            height, width = self.img.shape[:2]
            self.max_image_size = height * width

    def hide_bits(self):
        if self.max_image_size * 3 <= 2 * self.utils.get_payload_size(self.data):
            print('Can\'t Process')
        bitstream = iter(self.utils.text_to_binary(self.data, self.max_image_size * 3))

        height, width = self.img.shape[:2]
        blank_image = np.ones((height, width, 3), np.uint8)
        for row in range(height):
            for col in range(width):
                red, green, blue = self.img[row, col]
                rb = next(bitstream)

                red = self.utils.set_bit(red, rb)

                gb = next(bitstream)
                green = self.utils.set_bit(green, gb)

                bb = next(bitstream)
                blue = self.utils.set_bit(blue, bb)

                blank_image[row, col] = [red, green, blue]
        display_img(blank_image)
        plt.hist(blank_image.ravel(), 256, [0, 256])
        plt.show()
        cv2.imwrite(self.save_dir, blank_image)

    def extract_bits(self):
        height, width = self.img.shape[:2]
        hidden_data = ''
        for row in range(height):
            for col in range(width):
                red, green, blue = self.img[row, col]
                hidden_data += bin(red)[-1]

                hidden_data += bin(green)[-1]
                hidden_data += bin(blue)[-1]

        hidden_file = self.utils.reconstitute_from_binary(hidden_data, self.save_dir)
        return hidden_file


lsb = LSB(data_path='data/data.txt', image_path='img/cat.png', save_path='v.txt')
lsb.hide_bits()
