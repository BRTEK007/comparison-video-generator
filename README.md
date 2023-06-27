# comparison-video-generator
Generates a comparison video in a template from configuration file.

## screenshots
![](/screenshots/1.png)
![](/screenshots/2.png)
![](/screenshots/3.png)

## executing
```console
python3 generator.py --config=example/config.txt
```

## configuration file format
```
[path to first image]
[path to second image]
[empty line]
[first name]
[second name]
[empty line]
[category name][whitespace]['1' or '2' or '0' for draw]
```

## dependencies
MoviePy: https://github.com/Zulko/moviepy \
Pillow: https://github.com/python-pillow/Pillow/
NumPy: https://github.com/numpy/numpy