from itertools import chain

from kivy.graphics.texture import Texture


class Gradient(object):
    """
    Utility class for creating horizontal and vertical gradient textures.

    This class provides static methods to generate gradient textures either
    horizontally or vertically, based on the provided colors. It is primarily
    used in graphical rendering contexts where gradient textures are needed.
    """
    @staticmethod
    def horizontal(*args):
        """
        Generates a horizontal gradient texture using the provided colors.

        This method creates a gradient based on the RGBA values provided as arguments.
        Each color should be represented as a tuple of four floats in the range [0, 1],
        corresponding to red, green, blue, and alpha channels. The resulting texture
        is configured to display the gradient horizontally.

        :param args: The colors to use for the gradient, each represented as a tuple
            of four floats (red, green, blue, alpha). At least one color must be provided.
        :type args: tuple[float, float, float, float]
        :raises ValueError: If no colors are provided in the arguments.
        :return: A `Texture` object containing the horizontal gradient.
        :rtype: Texture
        """
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
        """
        Creates a vertical gradient texture from the provided colors. The gradient is composed
        of the colors given as arguments and interpolates between them vertically.

        :param args: A variable number of colors specified as tuples of RGBA values
                     (each component should be in the range [0.0, 1.0]). A minimum of
                     one color is required. If multiple colors are provided, the gradient
                     will interpolate between them.
        :type args: tuple
        :return: A Texture object representing the vertical gradient. The texture will
                 have interpolated UV position and size based on the number of colors
                 provided.
        :rtype: Texture
        :raises ValueError: If no colors are provided.
        """
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


def save_pixel_as_png(width, height, pixel_data, filename=None):
    """
    Generates a PNG image byte sequence based on given pixel data and saves it to
    a file if a filename is provided.

    This function constructs a PNG image file by assembling the required PNG
    chunks: IHDR, IDAT, and IEND. It generates the image bytes and writes them
    to a specified file if a valid filename is provided.

    :param width: The width of the image in pixels.
    :type width: int
    :param height: The height of the image in pixels.
    :type height: int
    :param pixel_data: A byte sequence containing the pixel data of the image.
        Each pixel should be represented by four bytes (RGBA format).
    :type pixel_data: bytes
    :param filename: The optional filename where the PNG file will be saved. If
        not provided, the generated PNG data will not be saved to disk.
    :type filename: str or None
    :return: A byte sequence representing the constructed PNG image.
    :rtype: bytes

    """
    # Prepare PNG header
    png_header = b'\x89PNG\r\n\x1a\n'

    # IHDR chunk
    ihdr = (
            struct.pack(">I", width)
            + struct.pack(">I", height)
            + b'\x08\x06\x00\x00\x00'
    )
    ihdr_crc = struct.pack(
        ">I",
        zlib.crc32(b'IHDR' + ihdr) & 0xffffffff
    )
    ihdr_chunk = (
            struct.pack(">I", len(ihdr))
            + b'IHDR' + ihdr + ihdr_crc
    )

    # IDAT chunk
    # Rearrange the pixels into scanlines
    scanlines = b''.join(
        b'\x00' + pixel_data[4 * i * width: 4 * (i + 1) * width]
        for i in range(height)
    )
    compressed_data = zlib.compress(scanlines)
    idat_crc = struct.pack(
        ">I",
        zlib.crc32(b'IDAT' + compressed_data) & 0xffffffff
    )
    idat_chunk = (
            struct.pack(">I", len(compressed_data))
            + b'IDAT' + compressed_data + idat_crc
    )

    # IEND chunk
    iend_chunk = (
            struct.pack(">I", 0)
            + b'IEND'
            + struct.pack(">I", zlib.crc32(b'IEND') & 0xffffffff)
    )

    image_byte = png_header + ihdr_chunk + idat_chunk + iend_chunk

    # Write all chunks to the file
    if filename:
        with open(filename, 'wb') as f:
            f.write(png_header)
            f.write(ihdr_chunk)
            f.write(idat_chunk)
            f.write(iend_chunk)

    return image_byte
