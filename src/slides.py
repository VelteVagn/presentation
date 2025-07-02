#!/usr/bin/env python3

# imports
import curses
import yaml
import argparse

# parse potential arguments: 
parser = argparse.ArgumentParser(
        description="Create a text-based presentation."
    )
parser.add_argument("-b", "--bulletpoint", help="Alter bulletpoints")
parser.add_argument("content", help=".yaml file with slide content")
parser.add_argument("-n", "--nobulletpoints", action="store_true", default=False)

args = parser.parse_args()

# read configurations:
with open("style/config.yaml") as file:
    configs = yaml.safe_load(file)

# set bulletpoint character. -b flag overrides config.yaml
if not args.nobulletpoints: # -n flag overrides -b flag and config.yaml
    if args.bulletpoint is None:
        bulletpoint = configs["bulletpoint"]
    else:
        bulletpoint = args.bulletpoint
    # make sure bulletpoints are of length 1
    if len(bulletpoint) != 1:
        raise ValueError("Bullet point must be single character (see config.yaml)")

# set colours from config.yaml:
t_bg = configs["colours"]["title_bkgd"] # title background colour
b_bg = configs["colours"]["text_bkgd"] # main body background colour
t_txt = configs["colours"]["title_colr"] # title text colour
b_txt = configs["colours"]["text_colr"] # main body text colour


def create_slide(stdscr, title, text):
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
    title_coor = (width - title_width) // 2  # title coordinates (centered)
    titlewin = curses.newwin(3, width, 1, 0)  # title banner
    textwin = curses.newwin(height-6, width-indent, 5, indent)  # text window

    # add underlined and ALL-CAPS title
    titlewin.addstr(1, title_coor, title.upper(), curses.A_UNDERLINE)

    # set background colours:
    titlewin.bkgd(' ', curses.color_pair(1))
    textwin.bkgd(' ', curses.color_pair(2))

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

    while True:
        key = stdscr.getch() # wait for input

        # refresh windows:
        titlewin.clear()
        titlewin.refresh()
        textwin.clear()
        textwin.refresh()
        #stdscr.refresh()

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

    # load slide content from content.yaml
    with open(args.content) as file:
        slides = yaml.safe_load(file)

    total_slides = len(slides["slides"]) # amount of slides

    # navigate between slides:
    n = 0 # current slide number

    while True:
        # update slide content:
        try:
            title = slides["slides"][n]["title"]
            bulletpoints = slides["slides"][n]["bulletpoints"]
        except IndexError:
            title = "fin"
            bulletpoints = ""

        # create slide and determine next action:
        next_action = create_slide(stdscr, title, bulletpoints)
        
        # if going to next slide and it exists:
        if next_action == "next" and n < total_slides:
            n += 1 # increase page number

        # if going to the previous slide and it doesn't exist:
        elif next_action == "prev" and n <= 0:
            n = 0 # let slide number remain at 0

        # if going to the previous slide and it exists:
        elif next_action == "prev" and n > 0:
            n -= 1 # decrease page number

        # if going to the next slide, but it doesn't exist
        elif next_action == "next" and n >= total_slides:
            break # break the loop, effectively ending the script


if __name__ == "__main__":
    curses.wrapper(main)
