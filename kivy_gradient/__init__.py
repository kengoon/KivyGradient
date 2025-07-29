from itertools import chain
from math import cos, sin, radians

from kivy.graphics.texture import Texture

class Gradient(object):

    @staticmethod
    def horizontal(*args):
        texture = Texture.create(size=(len(args), 1), colorfmt='rgba')
        buf = bytes([int(v * 255) for v in chain(*args)])  # flattens

        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture

    @staticmethod
    def vertical(*args):
        texture = Texture.create(size=(1, len(args)), colorfmt='rgba')
        buf = bytes([int(v * 255) for v in chain(*args)])  # flattens
        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture
        
    @staticmethod
    def angled(colors, size=(256, 256), angle=0):
        """
        Creates a texture with a gradient at an arbitrary angle.
        :param colors: List of colors (r, g, b, a) between 0.0 and 1.0.
        :param size: (width, height) of the texture.
        :param angle: Angle of the gradient in degrees (0 = left to right).
        :return: Texture
        """
        w, h = size
        texture = Texture.create(size=size, colorfmt='rgba')
        texture.mag_filter = 'linear'

        # Direção do gradiente
        angle_rad = radians(angle)
        dx = cos(angle_rad)
        dy = sin(angle_rad)

        buf = bytearray(w * h * 4)
        num_colors = len(colors) - 1

        for y in range(h):
            for x in range(w):
                # Normaliza posição (0 a 1) na direção do vetor (dx, dy)
                u = (x / w - 0.5) * dx + (y / h - 0.5) * dy + 0.5
                u = min(max(u, 0), 1)

                # Encontra as duas cores entre as quais interpolar
                pos = u * num_colors
                i = int(pos)
                frac = pos - i
                c1 = colors[i]
                c2 = colors[min(i + 1, num_colors)]

                rgba = [
                    int(255 * min(max(c1[j] + frac * (c2[j] - c1[j]), 0.0), 1.0))
                    for j in range(4)
                ]
                index = 4 * (y * w + x)
                buf[index:index + 4] = bytes(rgba)

        texture.blit_buffer(bytes(buf), colorfmt='rgba', bufferfmt='ubyte')
        return texture
