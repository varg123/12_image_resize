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
    return parser.parse_args()


def calculate_new_size(old_width, old_height, new_width=None, new_height=None, scale=None):
    if scale and (new_height or new_height):
        raise ValueError("Нельзя указывать мастаб и размеры одновременно")
    if scale:
        return int(old_width*scale), int(old_height*scale)
    if new_height and not new_width:
        scale = old_height/new_height
        return int(old_width), int(old_height*scale)
    elif not new_height and new_width:
        scale = old_width/new_width
        return int(old_width*scale), int(old_height*scale)
    elif new_height and new_width:
        return new_width, new_height
    return old_width, old_height


def create_image_path(input_path,  *size, output_path=None):
    if output_path:
        return output_path
    else:
        root, ext = os.path.splitext(input_path)
        return "{}__{}x{}{}".format(root, *size, ext)


def main():
    input_args = parse_args()
    try:
        img = Image.open(input_args.image)
        new_size = calculate_new_size(
            *img.size,
            input_args.width,
            input_args.height,
            input_args.scale
        )
        img = img.resize(new_size)
        image_path = create_image_path(
            input_args.image,
            *new_size,
            output_path=input_args.output
        )
        img.save(image_path)
    except FileNotFoundError:
        exit("Файл или дирректория не найдены")
    except OSError:
        exit("Файл не поддерживается")
    except ValueError:
        exit("Не корректные значения итоговых размеров")
    print("Изображение создано")


if __name__ == '__main__':
    main()
