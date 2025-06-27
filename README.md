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

Navigate using the left and right arrow keys, alternatively go to next slide with Enter.

If you want to custom bulletpoints, simply use the flag -b followed by you're preferred bullet point style, for example "-":
```bash
./src/slides.py -b "-" ~/path/to/slideshow.yaml
```
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
