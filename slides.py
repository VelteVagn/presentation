#!/usr/bin/env python3

# imports
import curses
import yaml

def create_slide(stdscr, title, text):
    curses.init_color(10, 639, 835, 1000)
    curses.init_color(11, 850, 940, 1000)
    curses.init_pair(1, curses.COLOR_BLUE, 10)
    curses.init_pair(2, curses.COLOR_BLUE, 11)
    height, width = stdscr.getmaxyx()
    indent = 3
    title_width = len(title)
    title_coor = (width - title_width) // 2
    titlewin = curses.newwin(3, width, 1, 0)
    titlewin.addstr(1, title_coor, title.upper())
    titlewin.addstr(2, title_coor, f"{'\u203E'*title_width}")
    textwin = curses.newwin(height-5, width-indent, 5, indent)
    titlewin.bkgd(' ', curses.color_pair(1))
    textwin.bkgd(' ', curses.color_pair(2))
    for row, line in enumerate(text):
        textwin.addstr(row, 0, line)
    textwin.refresh()
    titlewin.refresh()
    while True:
        key = stdscr.getch()
        if key in (curses.KEY_RIGHT, 32, curses.KEY_ENTER, 10, 13):
            titlewin.clear()
            titlewin.refresh()
            textwin.clear()
            textwin.refresh()
            return "next"
        elif key == curses.KEY_LEFT:
            titlewin.clear()
            titlewin.refresh()
            textwin.clear()
            textwin.refresh()
            return "prev"



def main(stdscr):

    curses.init_color(11, 850, 940, 1000)
    curses.init_pair(2, curses.COLOR_BLUE, 11)
    stdscr.bkgd(' ', curses.color_pair(2))

    curses.curs_set(0) # hide cursor

    stdscr.refresh()
    height, width = stdscr.getmaxyx()

    with open("content.yaml") as file:
        slides = yaml.safe_load(file)

    next_action = create_slide(stdscr, slides["slides"][0]["title"], slides["slides"][0]["bulletpoints"])
    n = 0 # current slide number
    total_slides = len(slides["slides"])
    while True:
        if next_action == "next" and n < total_slides-1:
            n += 1
            next_action = create_slide(stdscr, slides["slides"][n]["title"], slides["slides"][n]["bulletpoints"])
        elif next_action == "next" and n == total_slides-1:
            n += 1
            next_action = create_slide(stdscr, "Fin", "")
        elif next_action == "next" and n > total_slides-1:
            break
        elif next_action == "prev" and n <= 0:
            n = 0
            next_action = create_slide(stdscr, slides["slides"][n]["title"], slides["slides"][n]["bulletpoints"])
        elif next_action == "prev" and n > 0:
            n -= 1
            next_action = create_slide(stdscr, slides["slides"][n]["title"], slides["slides"][n]["bulletpoints"])



if __name__ == "__main__":
    curses.wrapper(main)
