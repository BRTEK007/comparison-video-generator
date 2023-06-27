import argparse
from moviepy.editor import *
from PIL import Image
import numpy as np

def get_images(path1, path2):
    img1 = Image.open(path1)
    img2 = Image.open(path2)
    img1 = img1.resize((720, 640))
    img2 = img2.resize((720, 640))
    return img1, img2

def get_single_slide(img):
    out_width = img.width 
    out_height = img.height*2
    out = Image.new('RGB', (out_width, out_height))
    out.paste(img, (0, int(img.height/2)))
    return np.array(out)

def get_joined_slide(img1, img2):
    out_width = img1.width 
    out_height = img1.height + img2.height
    out = Image.new('RGB', (out_width, out_height))
    out.paste(img1, (0, 0))
    out.paste(img2, (0, img1.height))
    return np.array(out)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='path to the config file', required=True)

    args = parser.parse_args()

    print(args.config)

    img1, img2 = get_images('example/zebra.jpg', 'example/turtle.jpg')
    single_slide_1 = get_single_slide(img1)
    single_slide_2 = get_single_slide(img2)
    joined_slide = get_joined_slide(img1, img2)

    single_clip_1 = ImageClip(single_slide_1).set_duration(1)
    single_clip_2 = ImageClip(single_slide_2).set_duration(1)
    joined_clip = ImageClip(joined_slide).set_duration(1)

    result = concatenate_videoclips([joined_clip, single_clip_1, single_clip_2])
    result.write_videofile('out.mp4',fps=30)

if __name__ == '__main__':
    main()