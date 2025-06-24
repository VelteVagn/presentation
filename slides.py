#!/usr/bin/env python3

# imports
import curses

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
    content1 = [
            "",
            "\u2022 Bachelor i matematikk i Lund",
            " - Tallteori",
            " - Algebra",
            " - Filosofi, historie, informasjonssikkerhet, osv",
            "",
            "\u2022 Master i logikk i Göteborg",
            " - Mengdeteori",
            " - Modellteori",
            " - Logisk teori",
            " - Kryptografi",
            ]
    content2 = [
            "",
            "\u2022 Programmering (Python)",
            "",
            "\u2022 Snekring",
            "",
            "\u2022 Kreativ skriving",
            ]
    
    content3 = [
            "",
            "\u2022 Lucas–Lehmer:",
            "",
            "   Hvis p > 2 er et primtall, så er P = 2^p - 1 primtall hvis og bare hvis",
            "",
            "   \u03b5^(2^(p-1)) \u2261 -1 (mod P)",
            "",
            "   hvor \u03b5 = 2 + sqrt(3).",
            "",
            "\u2022 Generalisert versjon",
            ]
    content4 = [
            "",
            "\u2022 Problem:",
            "    Bruker for mye på den lokale matbutikken.",
            "",
            "\u2022 Løsning:",
            "    Notér ned hvert eneste kjøp.",
            "",
            "\u2022 Metode:",
            "   - Scanne alle digitale kvitteringene med KI.",
            "   - Registrere hvert varekjøp (produkt, mengde, pris).",
            "   - Dobbeltsjekke at totalpris og mengde stemmer overrens med kvitteringa.",
            "   - Putte hver nye produkt i en kategori (grønnsaker, meieri, brød, osv).",
            "   - Registrere alle kjøp i en SQL-tabell.",
            "",
            "\u2022 Jo flere produkter som allerede er registrerte, jo fortere går programmet.",
            "",
            ]
    content5 = [
            "",
            "\u2022 Linux",
            "",
            "\u2022 Network-attached storage",
            "",
            "\u2022 Spisebord",
            "",
            "\u2022 Battleship",
            ]

    slide1 = ("Bakgrunn", content1)
    slide2 = ("Interesser", content2)
    slide3 = ("Bacheloroppgaven", content3)
    slide4 = ("Kvitteringsregister", content4)
    slide5 = ("Neste prosjekt", content5)

    slides = (slide1, slide2, slide3, slide4, slide5)
    next_action = create_slide(stdscr, slide1[0], slide1[1])
    n = 0 # current slide number
    total_slides = len(slides)
    end = False
    while not end:
        if next_action == "next" and n < total_slides-1:
            n += 1
            next_action = create_slide(stdscr, slides[n][0], slides[n][1])
        elif next_action == "next" and n == total_slides-1:
            n += 1
            next_action = create_slide(stdscr, "Fin", "")
        elif next_action == "next" and n > total_slides-1:
            break
        elif next_action == "prev" and n <= 0:
            n = 0
            next_action = create_slide(stdscr, slides[n][0], slides[n][1])
        elif next_action == "prev" and n > 0:
            n -= 1
            next_action = create_slide(stdscr, slides[n][0], slides[n][1])



if __name__ == "__main__":
    curses.wrapper(main)
