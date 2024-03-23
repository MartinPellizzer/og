
from PIL import Image, ImageFont, ImageDraw, ImageColor


# def img_resize(image_path):
#     w, h = 768, 512

#     img = Image.open(image_path)

#     start_size = img.size
#     end_size = (w, h)

#     if start_size[0] / end_size [0] < start_size[1] / end_size [1]:
#         ratio = start_size[0] / end_size[0]
#         new_end_size = (end_size[0], int(start_size[1] / ratio))
#     else:
#         ratio = start_size[1] / end_size[1]
#         new_end_size = (int(start_size[0] / ratio), end_size[1])

#     img = img.resize(new_end_size)

#     w_crop = new_end_size[0] - end_size[0]
#     h_crop = new_end_size[1] - end_size[1]
    
#     area = (
#         w_crop // 2, 
#         h_crop // 2,
#         new_end_size[0] - w_crop // 2,
#         new_end_size[1] - h_crop // 2
#     )
#     img = img.crop(area)

#     output_path = image_path.replace('articles', 'articles-images')
#     output_path = f'public/assets/images/{"-".join(image_path.split("/")[2:])}'
#     img.save(f'{output_path}')

#     return output_path


# def generate_featured_image(attribute, attr_2):
#     industry_formatted = industry.replace(' ', '-')
#     image_path_in = f'articles-images/public/ozono/sanificazione/{attribute}/{industry_formatted}/featured.jpg'
#     image_filename_out = f'{attribute.replace("/", "-")}-{industry_formatted}-featured.jpg'
#     image_filepath_out = f'/assets/images/{image_filename_out}'
#     image_path_out = f'public/assets/images/{image_filename_out}'
#     util_img.resize(image_path_in, image_path_out)

#     return image_filepath_out


def resize(image_path_in, image_path_out):
    w, h = 768, 576

    img = Image.open(image_path_in)

    start_size = img.size
    end_size = (w, h)

    if start_size[0] / end_size [0] < start_size[1] / end_size [1]:
        ratio = start_size[0] / end_size[0]
        new_end_size = (end_size[0], int(start_size[1] / ratio))
    else:
        ratio = start_size[1] / end_size[1]
        new_end_size = (int(start_size[0] / ratio), end_size[1])

    img = img.resize(new_end_size, Image.Resampling.LANCZOS)

    w_crop = new_end_size[0] - end_size[0]
    h_crop = new_end_size[1] - end_size[1]
    
    area = (
        w_crop // 2, 
        h_crop // 2,
        new_end_size[0] - w_crop // 2,
        new_end_size[1] - h_crop // 2
    )
    img = img.crop(area)

    output_path = image_path_out
    img.save(output_path, quality=100)

    return output_path


def gen_plain(image_path, w, h, image_path_out):
    img = Image.open(image_path)

    start_size = img.size
    end_size = (w, h)

    if start_size[0] / end_size [0] < start_size[1] / end_size [1]:
        ratio = start_size[0] / end_size[0]
        new_end_size = (end_size[0], int(start_size[1] / ratio))
    else:
        ratio = start_size[1] / end_size[1]
        new_end_size = (int(start_size[0] / ratio), end_size[1])

    img = img.resize(new_end_size)

    w_crop = new_end_size[0] - end_size[0]
    h_crop = new_end_size[1] - end_size[1]
    
    area = (
        w_crop // 2, 
        h_crop // 2,
        new_end_size[0] - w_crop // 2,
        new_end_size[1] - h_crop // 2
    )
    img = img.crop(area)

    name = image_path.split('/')[-1]
    path = image_path.split('/')[:-1]
        
    img.save(f'{image_path_out}')

