# Slides

If you want a simple tool to present colourful slides, you've come to the right place. 

## Usage

Create a .yaml file with similar structure as `examples/example_presentation.yaml`, e.g., `slideshow.yaml`. Navigate to the project folder
```bash
cd slides
```
and run the script
```bash
./src/slides.py ~/path/to/slideshow.yaml
```

### Navigation

Navigate using the left and right arrow keys, alternatively go to next slide with Enter. Exit by pressing capital Q, or Ctrl + C.

### Optional flags

#### `-b, --bulletpoints`

If you want to custom bulletpoints, simply use the flag `-b` followed by you're preferred bullet point style, for example "-":
```bash
./src/slides.py -b "-" ~/path/to/slideshow.yaml
```
To permanently change the bulletpoints, change the variable named `bulletpoint`.

Note that bulletpoints must be one character long in current version.

#### `-c, --colour, --color`

Change the colours to a predefined colour scheme, e.g.,
```bash
./src/slides.py -c red ~/path/to/slideshow.yaml
```
In this version, the following colour schemes exist:
- `blue, b`
- `red, r`
- `green, g`
- `black, l`
- `yellow, y`

To permanently change the colours, change the variable named colours in `style/config.yaml`. To see the codes for the predefined colour schemes, check out `style/colour\_schemes.yaml`.

#### `-h, --help`

Show a description of the possible flags. 

#### `-n, --nobulletpoints`

Toggles off bullet points. Paragraphs will still be generated as before, just without the bullet points.

#### `--nofinale`

Toggles off the final slide. 

#### `--notitle`

Toggles off the title screen. If `-p` flag is used, `--notitle` will be overridden.

#### `-p, --pages`

Takes one or more integers as arguments. Shows slides by page number in order given. 0 represents the title slide, 1 the first slide, 2 the second slide, etc. Can be used to check specific slides or changing the order. Example:
```bash
./src/slides.py ~/path/to/slideshow.yaml -p 0 3 2 1
```
Will show the title screen, and then the three first slides in reverse order. Note that because `-p` takes multiple arguments, it must be the last flag, even after the path to the `.yaml` file. 

## License

This project is licensed under the [GNU General Public License](COPYING).

## Notes

As the terminal is strictly text based, so will any presentation be, with the exception of text art like ASCII art, naturally. 

This program assumes your terminal can handle all the colours. If
```bash
$ echo $TERM
output: xterm-256color
```
your terminal should manage. If your terminal doesn't support enough colours, the presentations would probably not look good anyway.

It is highly recommended to increase the text size in the terminal. Otherwise, the text will most likely look too small compared to the screen.

In the current version, there is no auto-indentation, meaning long lines must be indented manually in the config.yaml file. Otherwise the program will crash given if the terminal window is not sufficiently big.
