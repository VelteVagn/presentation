#!/usr/bin/env python3

# imports
import curses
import yaml
import argparse
from collections.abc import Iterable

# parse arguments: 
parser = argparse.ArgumentParser(
        description="Create a text-based presentation."
    )

parser.add_argument(
        "-b", "--bulletpoint",
        help="Alter bulletpoints",
    )
parser.add_argument(
        "-n", "--nobulletpoints",
        action="store_true",
        default=False,
    )
parser.add_argument(
        "-p", "--pages", 
        nargs="+", 
        help="Pages to include",
    )
parser.add_argument(
        "-c", "--colour", "--color",
        help="Choose predefined colour scheme",
    )
parser.add_argument(
        "--notitle",
        action="store_true",
        default=False,
        help="Toggle off title slide",
    )
parser.add_argument(
        "--nofinale",
        action="store_true",
        default=False,
        help="Toggle off finale empty slide",
    )
parser.add_argument(
        "content",
        help=".yaml file with slide content",
    )

args = parser.parse_args()

notitle = args.notitle

nofinale = args.nofinale

# load the title
with open(args.content) as file:
    title = yaml.safe_load(file)['title']

# load style
with open('style/config.yaml') as file:
    configs = yaml.safe_load(file)

# set colour scheme if -c flag is included
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
    # otherwise use the colours from the config file
    colours = configs["colours"]

# set bulletpoint character
# -b flag overrides config.yaml
if not args.nobulletpoints: # -n flag overrides -b flag and config.yaml
    if args.bulletpoint is None:
        bulletpoint = configs["bulletpoint"]
    else:
        bulletpoint = args.bulletpoint
    # make sure bulletpoints are of length 1
    if len(bulletpoint) != 1:
        raise ValueError("Bullet point must be single character")

# make sure -p arguments are integers:
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

# set colours:
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

    # set background colours:
    titlewin.bkgd(' ', curses.color_pair(1))
    textwin.bkgd(' ', curses.color_pair(2))
    stdscr.bkgd(' ', curses.color_pair(2))
    
    # add underlined and ALL-CAPS title
    if title_slide:
        titlewin.addstr(
                height//10,
                title_coor,
                title.upper(),
                curses.A_UNDERLINE
            )
    else:
        titlewin.addstr(
                1,
                title_coor,
                title.upper(),
                curses.A_UNDERLINE
            )

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
                    indent = '' # no indent on empty lines
                elif line[0] == '\u2022':  
                    indent = '' # no indent on bullet points
                else:
                    indent = '  ' # indent lines without bullet points

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

        # quit on capital Q
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

    # load slide content from content.yaml
    with open(args.content) as file:
        content = yaml.safe_load(file)

    # amount of slides
    l = len(content['slides'])

    # create index lists of page numbers, e.g.:
    # ["t", 1, 2, ..., N] for all N slides including title screen
    # [1, 2, ..., N] for all N slides without title screen
    # [3, 5, 2, "t"] for 3rd, 5th, 2nd and title slides in that order
    try:
        # check for user specified page numbers
        pages = globals()["pages"]
        pages = ["t" if p == 0 else p-1 for p in pages] # reindex
        
        # make sure they're within the range
        if not all(0 <= p < l if isinstance(p, int) else True for p in pages):
            raise IndexError("Page numbers out of range")
    except KeyError:
        # else set all pages and alternatively title 
        pages = list(range(l))

        # add title unless explicitly or implicitly stated otherwise
        if not globals()['notitle'] and globals()['title'] != '':
            pages = ['t'] + pages 

    i = 0 # begin indexing at 0
    while True:
        title_slide = False # default slides are not title slides

        try:
            if pages[i] == "t":
                # configure title slide 
                title = content["title"]
                bulletpoints = ""
                title_slide = True
            else:
                # configure normal slides
                title = content["slides"][pages[i]]["title"]
                bulletpoints = content["slides"][pages[i]]["bulletpoints"]
        except IndexError:
            if globals()["nofinale"]:
                break
            else:
                # configure end slide
                title = "fin"
                bulletpoints = ""
        
        # create the slide and get next action from user input
        next_action = create_slide(stdscr, title, bulletpoints, title_slide)

        # change index based before next (or previous) slide
        match next_action:
            case "next":
                if i < len(pages):
                    i += 1
                else:
                    break
            case "prev":
                if i <= 0:
                    i = 0
                else:
                    i -= 1

if __name__ == "__main__":
    curses.wrapper(main)
