from PIL import Image
import argparse
import os.path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('image',  help='Path to source image.')
    parser.add_argument('-w', '--width', help='Desired width', type=int)
    parser.add_argument('-hg', '--height', help='Desired height', type=int)
    parser.add_argument('-s', '--scale', help='Desired scale', type=float)
    parser.add_argument('-o', '--output', help='Path to the finished image')
    input_args = parser.parse_args()
    if input_args.scale and input_args.scale < 0:
        parser.error('Invalid value of scale argument')
    if input_args.width and input_args.width < 0:
        parser.error('Invalid value of width option')
    if input_args.height and input_args.height < 0:
        parser.error('Invalid value of height option')
    if input_args.scale and (input_args.width or input_args.height):
        parser.error(
            'You cannot specify scale and dimensions at the same time'
        )
    if not (input_args.scale or input_args.width or input_args.height):
        parser.error(
            'One of the following parameters must be specified: -w, -hg or -s'
        )
    if os.path.isdir(input_args.image):
        parser.error('The specified path is directory')
    if input_args.output and os.path.isdir(input_args.output):
        parser.error('The specified path is directory')
    return input_args


def calculate_new_size_by_wh(old_width, old_height, new_width, new_height):
    scale = 0
    if new_height and not new_width:
        scale = old_height/new_height
        return int(old_width/scale), int(old_height/scale)
    elif not new_height and new_width:
        scale = old_width/new_width
        return int(old_width/scale), int(old_height/scale)
    elif new_height and new_width:
        return new_width, new_height
    return old_width, old_height


def calculate_new_size_by_scale(old_width, old_height, scale):
    return int(old_width*scale), int(old_height*scale)


def create_image_path(input_path, output_path, *size):
    if output_path:
        return output_path
    else:
        root, ext = os.path.splitext(input_path)
        return '{}__{}x{}{}'.format(root, *size, ext)


def main():
    input_args = parse_args()
    new_size = (input_args.width, input_args.height)
    try:
        img = Image.open(input_args.image)
        if input_args.scale:
            new_size = calculate_new_size_by_scale(*img.size, input_args.scale)
        else:
            new_size = calculate_new_size_by_wh(*img.size, *new_size)
        img = img.resize(new_size)
        image_path = create_image_path(
            input_args.image,
            input_args.output,
            *new_size
        )
        img.save(image_path)
    except FileNotFoundError:
        exit('The source image not found')
    except OSError:
        exit('The source is not valid image file')
    print('Изображение создано')


if __name__ == '__main__':
    main()
