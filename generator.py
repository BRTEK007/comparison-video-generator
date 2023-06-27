import argparse
import sys
from moviepy.editor import *
from PIL import Image
import numpy as np
import os

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

class Config:
    def __init__(self, path):
        try:
            config_file_dir = os.path.dirname(os.path.abspath(path))#absolute path to directory with config file
            with open(path, "r") as f:
                lines_raw = f.readlines()
                lines = list(map(lambda x : x.strip(), lines_raw))

                self.img_paths = [
                    os.path.abspath(os.path.join(config_file_dir, lines[0])),
                    os.path.abspath(os.path.join(config_file_dir, lines[1]))]
                
                self.names = [lines[3], lines[4]]

                self.comparisons = []

                for i in range(6, len(lines)):
                    line = lines[i]
                    line_split = line.split(' ')
                    category = line_split[0]
                    winner = int(line_split[1])-1
                    self.comparisons.append((category, winner))
        except:
            print('ERROR config file format', file=sys.stderr)
            exit(-1)

def get_text_clip(text):
    return (TextClip(text, size=(640, None),color='white', stroke_color='black', stroke_width=2)
                      .set_position('center')
                      .set_duration(1))

def generate_video(config):
    img1, img2 = get_images(config.img_paths[0], config.img_paths[1])
    single_slides = [get_single_slide(img1), get_single_slide(img2)]
    joined_slide = get_joined_slide(img1, img2)

    single_clips = list(map(lambda x: ImageClip(x).set_duration(1), single_slides))

    joined_clip = ImageClip(joined_slide).set_duration(1)

    intro_txt_clip = get_text_clip('{}\nvs\n{}'.format(config.names[0], config.names[1])) 

    intro_clip = CompositeVideoClip([joined_clip, intro_txt_clip])
    out_clip = concatenate_videoclips([intro_clip])

    scores = [0, 0]

    for category, winner in config.comparisons:
        scores[winner] += 1
        category_txt_clip = get_text_clip(category)
        score_txt_clip = get_text_clip('{}-{}'.format(scores[0], scores[1]))
        out_clip = concatenate_videoclips([out_clip, 
                                        CompositeVideoClip([joined_clip, category_txt_clip]),
                                        CompositeVideoClip([single_clips[winner], score_txt_clip])])
                                         
    final_winner = 0 if scores[0] > scores[1] else 1

    out_clip = concatenate_videoclips([out_clip, 
                CompositeVideoClip([joined_clip, get_text_clip('winner')]),
                CompositeVideoClip([single_clips[final_winner], get_text_clip('{}-{}'.format(scores[0], scores[1]))])])

    return out_clip

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='path to the config file', required=True)

    args = parser.parse_args()

    config = Config(args.config)

    video = generate_video(config)
    
    video.write_videofile('out.mp4',fps=2)

if __name__ == '__main__':
    main()