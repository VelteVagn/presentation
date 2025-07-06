#!/usr/bin/env python3

# imports
import curses
import yaml
import argparse
from collections.abc import Iterable

# parse potential arguments: 
parser = argparse.ArgumentParser(
        description="Create a text-based presentation."
    )
parser.add_argument("-b", "--bulletpoint", help="Alter bulletpoints")
parser.add_argument("-n", "--nobulletpoints", action="store_true", default=False)
parser.add_argument("-p", "--pages", nargs="+", help="Pages to include")
parser.add_argument("-c", "--colour", "--color", help="Choose predefined colour scheme")
parser.add_argument("--notitle", action="store_true", default=False, help="Toggle off title slide")
parser.add_argument("content", help=".yaml file with slide content")

args = parser.parse_args()

notitle = args.notitle

with open(args.content) as file:
    title = yaml.safe_load(file)['title']

# read configurations:
with open("style/config.yaml") as file:
    configs = yaml.safe_load(file)

if args.colour:
    match args.colour.lower():
        case "b" | "blue":
            colour = "blue"
        case "r" | "red":
            colour = "red"
        case "g" | "green":
            colour = "green"
        case "l" | "black":
            colour = "black"
        case "y" | "yellow":
            colour = "yellow"
        case _:
            raise KeyError("No such colour scheme.")

    with open("style/colour-schemes.yaml") as file:
        colours = yaml.safe_load(file)[colour]
else:
    colours = configs["colours"]

# set bulletpoint character. -b flag overrides config.yaml
if not args.nobulletpoints: # -n flag overrides -b flag and config.yaml
    if args.bulletpoint is None:
        bulletpoint = configs["bulletpoint"]
    else:
        bulletpoint = args.bulletpoint
    # make sure bulletpoints are of length 1
    if len(bulletpoint) != 1:
        raise ValueError("Bullet point must be single character (see config.yaml)")

if not args.pages is None:
    if isinstance(args.pages, Iterable):
        try:
            pages = [int(p) for p in args.pages]
        except ValueError:
            raise ValueError("--pages requires integers")
    else:
        try:
            pages = [int(args.pages)]
        except ValueError:
            raise ValueError("--pages requires integers")

# set colours from config.yaml:
t_bg = colours["title_bkgd"] # title background colour
b_bg = colours["text_bkgd"] # main body background colour
t_txt = colours["title_colr"] # title text colour
b_txt = colours["text_colr"] # main body text colour


def create_slide(stdscr, title, text, title_slide=False):
    """
    Create a new slide and wait for input.

    Args:
        stdscr (curses.window): main curses window
        title (str): title of the slide
        text (list): list of slide paragraphs

    Out:
        str: "next" or "prev" depending on user input
    """
    # constants:
    height, width = stdscr.getmaxyx() # screen height and width
    indent = 3 # indentation of main text
    title_width = len(title) # width of the title text
    title_coor = (width - title_width) // 2  # title x-coordinates (centered)
    if title_slide:
        titlewin = curses.newwin(height // 5, width, (height // 5)*2, 0)  # title banner
    else:
        titlewin = curses.newwin(3, width, 1, 0)  # title banner
    textwin = curses.newwin(height-6, width-indent, 5, indent)  # text window


    # refresh windows:
    stdscr.clear()
    stdscr.refresh()
    #titlewin.clear()
    #titlewin.refresh()
    #textwin.clear()
    #textwin.refresh()

    # set background colours:
    titlewin.bkgd(' ', curses.color_pair(1))
    textwin.bkgd(' ', curses.color_pair(2))
    stdscr.bkgd(' ', curses.color_pair(2))
    
    # add underlined and ALL-CAPS title
    if title_slide:
        titlewin.addstr(height//10, title_coor, title.upper(), curses.A_UNDERLINE)
    else:
        titlewin.addstr(1, title_coor, title.upper(), curses.A_UNDERLINE)

    if not title_slide:
        # add bullet points to paragraphs
        if not args.nobulletpoints:
            text = [f'{bulletpoint} {paragraph}' for paragraph in text]

        # split text into lines instead of paragraphs:

        # convert list to string with double linebreak between paragraphs
        text = '\n\n'.join(text)
        # convert string to list of lines instead of paragraphs
        text = text.split('\n')

        # add all text lines to the window:
        for row, line in enumerate(text):
            if args.nobulletpoints:
                indent = ''
            else:
                if line == '':
                    indent = ''
                elif line[0] == '\u2022':
                    indent = ''
                else:
                    indent = '  ' # indent lines without bullet points to align well
            textwin.addstr(row, 0, f'{indent}{line}') # add line to window

    # refresh windows
    textwin.refresh()
    titlewin.refresh()
    stdscr.refresh()

    while True:
        key = stdscr.getch() # wait for input


        # if input is <enter> or <right>, output "next"
        if key in (curses.KEY_RIGHT, 32, curses.KEY_ENTER, 10, 13):
            return "next"

        # if input is <left key>, return "prev"
        elif key == curses.KEY_LEFT:
            return "prev"

        # quit on Q
        elif key == 81:
            exit()


def main(stdscr):
    """
    Main function called by the curses wrapper.

    Args:
        stdscr (curses.window): main curses window

    Out:
        None 
    """

    # initialise colours:
    curses.init_color(1, t_bg[0], t_bg[1], t_bg[2])
    curses.init_color(2, b_bg[0], b_bg[1], b_bg[2])
    curses.init_color(3, t_txt[0], t_txt[1], t_txt[2])
    curses.init_color(4, b_txt[0], b_txt[1], b_txt[2])

    # initilise colour pairs:
    curses.init_pair(1, 3, 1)
    curses.init_pair(2, 4, 2)

    stdscr.bkgd(' ', curses.color_pair(2)) # set background colour

    curses.curs_set(0) # hide cursor

    stdscr.refresh() # initial refresh to start up

    height, width = stdscr.getmaxyx() # screen height and width

    if globals()['notitle'] or globals()['title'] == "":
        floor = 1 # smallest possible index 
        i = 1 # current index of pages
        t = 0 # number of title pages
    else:
        floor = 0 # smallest possible index
        i = 0 # current index of pages
        t = 1 # number of title pages 

    # load slide content from content.yaml
    with open(args.content) as file:
        slides = yaml.safe_load(file)

    total_slides = len(slides["slides"]) + t # amount of slides
    
    # create a list of page indexes
    try:
        pages = globals()["pages"] # get specified page numbers
    except KeyError:
        pages = list(range(floor, total_slides)) # include all pages otherwise
    
    # make sure pages given by -p flag are within bounds
    if not all(0 <= p < total_slides for p in pages):
        raise IndexError("page number out of range")

    # navigate between slides:
    while True:
        # update slide content:
        try:
            title = slides["slides"][pages[i]]["title"]
            bulletpoints = slides["slides"][pages[i]]["bulletpoints"]
        except IndexError:
            title = "fin"
            bulletpoints = ""

        if i == 0:
            title_slide = True
        else:
            title_slide = False

        # create slide and determine next action:
        next_action = create_slide(stdscr, title, bulletpoints, title_slide)
        
        # if going to next slide and it exists:
        if next_action == "next" and i + 1 < len(pages) + floor:
            i += 1 # increase page number

        # if going to the previous slide and it doesn't exist:
        elif next_action == "prev" and i <= floor:
            i = floor # let slide number remain at 0

        # if going to the previous slide and it exists:
        elif next_action == "prev" and i > floor:
            i -= 1 # decrease page number

        # if going to the next slide, but it doesn't exist
        elif next_action == "next" and i + 1 >= len(pages) + floor:
            break # break the loop, effectively ending the script


if __name__ == "__main__":
    curses.wrapper(main)
