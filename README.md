# comparison-video-generator
Generates a comparison video in a template from configuration file.

## executing
```console
python3 generator.py --config=example/config.txt
```

## configuration file format
```
[path to first image]
[path to second image]
[empty line]
[category name][whitespace]['1' or '2' or '0' for draw]
```

## dependencies
moviepy: https://github.com/Zulko/moviepy