from itertools import chain

from kivy.graphics.texture import Texture


class Gradient(object):

    @staticmethod
    def horizontal(*args):
        if not args:
            raise ValueError('Gradient.horizontal() requires at least one color')
        size = len(args)
        texture = Texture.create(size=(size, 1), colorfmt='rgba')
        buf = bytes([int(v * 255) for v in chain(*args)])  # flattens

        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')

        if size < 2:
            return texture

        texture.uvpos = (0.5 / size, 0)
        texture.uvsize = ((size - 1) / size, 1)
        return texture

    @staticmethod
    def vertical(*args):
        if not args:
            raise ValueError('Gradient.vertical() requires at least one color')
        size = len(args)
        texture = Texture.create(size=(1, size), colorfmt='rgba')
        buf = bytes([int(v * 255) for v in chain(*args)])  # flattens

        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')

        if size < 2:
            return texture

        texture.uvpos = (0, 0.5 / size)
        texture.uvsize = (1, (size - 1) / size)
        return texture
