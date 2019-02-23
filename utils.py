import struct
def hex_to_rgb(rgb):
    return [item/255.0 for item in struct.unpack('BBB', rgb.decode('hex'))] + [1]
