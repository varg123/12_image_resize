from PIL import Image
import argparse
import os.path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('image',  help='This will be option One')
    parser.add_argument('-w', '--width', help='This will be option One', type=int)
    parser.add_argument('-hg', '--height', help='This will be option two', type=int)
    parser.add_argument('-s', '--scale', help='This will be option three', type=float)
    parser.add_argument('-o', '--output', help='This will be option three')
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
    except FileNotFoundError:
        exit("Файл не найден")
    except OSError:
        exit("Файл не поддерживается")
    new_size = calculate_new_size(
        *img.size,
        input_args.width,
        input_args.height,
        input_args.scale
    )
    try:
        img = img.resize(new_size)
    except ValueError:
        exit("Не корректные значения итоговых размеров")
    image_path = create_image_path(
        input_args.image,
        *new_size,
        output_path=input_args.output
    )
    try:
        img.save(image_path)
    except FileNotFoundError:
        exit("Не удалось сохранить. Проверьте существование пути")
    print("Изображение создано")


if __name__ == '__main__':
    main()
