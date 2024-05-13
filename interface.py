import curses
import datetime
import csv
import textwrap

LIBRARY_CSV = 'library.csv'
HIGHLIGHT_COLOR_PAIR = 1

def search_books(search_term):
    try:
        with open(LIBRARY_CSV, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            matches = [row for row in reader if search_term.lower() in row['Book title'].lower()]
            return matches
    except FileNotFoundError:
        return None

def search_books_by_author(search_term):
    try:
        with open(LIBRARY_CSV, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            matches = [row for row in reader if search_term.lower() in row['Book Author'].lower()]
            return matches
    except FileNotFoundError:
        return None

def search_books_by_description(search_term):
    try:
        with open(LIBRARY_CSV, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            matches = [row for row in reader if search_term.lower() in row['Book Description'].lower()]
            return matches
    except FileNotFoundError:
        return None


def display_search_results(stdscr, results, current_page):
    max_y, max_x = stdscr.getmaxyx()

    if current_page < len(results):
        result = results[current_page]
        title = f"Title: {result['Book title']}"
        author = f"Author: {result['Book Author']}"
        description = f"Description: {result['Book Description']}"
        wrapped_description = textwrap.fill(description, width=max_x - 1)
        stdscr.addstr(4, 1, title)
        stdscr.addstr(5, 1, author)
        stdscr.addstr(6, 1, wrapped_description)

    page_info = f"Page {current_page + 1} of {len(results)}"
    stdscr.addstr(max_y - 2, (max_x - len(page_info)) // 2, page_info)

    if current_page < len(results) - 1:
        stdscr.addstr(max_y - 1, 1, "Press 'n' for next page, 'p' for previous page, or any other key to return.")
    else:
        stdscr.addstr(max_y - 1, 1, "Press 'p' for previous page or any other key to return.")


def main(stdscr):
    curses.noecho()
    curses.cbreak()
    max_y, max_x = stdscr.getmaxyx()
    curses.init_pair(HIGHLIGHT_COLOR_PAIR, curses.COLOR_BLACK, curses.COLOR_WHITE)
    highlight_text = curses.color_pair(HIGHLIGHT_COLOR_PAIR)

    while True:
        stdscr.clear()

        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        time_str = datetime.datetime.now().strftime("%H:%M:%S")
        stdscr.addstr(1, 1, date_str, highlight_text)
        stdscr.addstr(1, max_x - len(time_str) - 1, time_str, highlight_text)

        header = "MANGO TOWN PUBLIC LIBRARY"
        stdscr.addstr(3, (max_x - len(header)) // 2, header, highlight_text)

        welcome_msg = "Welcome to the Online Public Access Catalog!"
        stdscr.addstr(5, (max_x - len(welcome_msg)) // 2, welcome_msg)

        instructions = "Please select one of the options below:"
        stdscr.addstr(6, (max_x - len(instructions)) // 2, instructions)

        menu_items = ["Search by title", "Search by author", "Search by description", "Exit"]
        menu_start = (max_y - len(menu_items)) // 2
        longest_item = max(menu_items, key=len)
        start_col = (max_x - len(longest_item)) // 2

        for index, item in enumerate(menu_items):
            stdscr.addstr(menu_start + index, start_col, f"{index + 1}. {item}")

        stdscr.addstr(max_y - 2, 1, "Enter your selection and press <Enter>: ")
        stdscr.refresh()
        curses.echo()  # Enable echoing of typed characters
        choice = stdscr.getstr(max_y - 2, 42, 3).decode().strip()  # Adjusted position
        curses.noecho()  # Disable echoing of typed characters

        if choice == '1':
            stdscr.clear()
            stdscr.addstr(1, 1, "Enter search term for book titles:")
            stdscr.refresh()
            curses.echo()  # Enable echoing of typed characters
            search_term = stdscr.getstr(2, 1, 20).decode().strip()
            curses.noecho()  # Disable echoing of typed characters

            results = search_books(search_term)
            if results is None:
                stdscr.addstr(4, 1, "Error: Could not open library CSV file.")
            elif results:
                current_page = 0
                while True:
                    stdscr.clear()
                    display_search_results(stdscr, results, current_page)
                    stdscr.refresh()
                    key = stdscr.getkey()
                    if key == 'n' and current_page < len(results) - 1:
                        current_page += 1
                    elif key == 'p' and current_page > 0:
                        current_page -= 1
                    else:
                        break
            else:
                stdscr.addstr(4, 1, "No matches found.")
                stdscr.addstr(max_y - 1, 1, "Press any key to return.")
                stdscr.getch()
        elif choice == '2':
            stdscr.clear()
            stdscr.addstr(1, 1, "Enter search term for book authors:")
            stdscr.refresh()
            curses.echo() # Enable echoing of typed characters  
            search_term = stdscr.getstr(2, 1, 20).decode().strip()
            curses.noecho() # Disable echoing of typed characters
            results = search_books_by_author(search_term)
            if results is None:
                stdscr.addstr(4, 1, "Error: Could not open library CSV file.")
            elif results:
                current_page = 0
                while True:
                    stdscr.clear()
                    display_search_results(stdscr, results, current_page)
                    stdscr.refresh()
                    key = stdscr.getkey()
                    if key == 'n' and current_page < len(results) - 1:
                        current_page += 1
                    elif key == 'p' and current_page > 0:
                        current_page -= 1
                    else:
                        break
            else:
                stdscr.addstr(4, 1, "No matches found.")
                stdscr.addstr(max_y - 1, 1, "Press any key to return.")
                stdscr.getch()
        elif choice == '3':
            stdscr.clear()
            stdscr.addstr(1, 1, "Enter search term for book descriptions:")
            stdscr.refresh()
            curses.echo()  # Enable echoing of typed characters
            search_term = stdscr.getstr(2, 1, 20).decode().strip()
            curses.noecho()  # Disable echoing of typed characters
            results = search_books_by_description(search_term)
            if results is None:
                stdscr.addstr(4, 1, "Error: Could not open library CSV file.")
            elif results:
                current_page = 0
                while True:
                    stdscr.clear()
                    display_search_results(stdscr, results, current_page)
                    stdscr.refresh()
                    key = stdscr.getkey()
                    if key == 'n' and current_page < len(results) - 1:
                        current_page += 1
                    elif key == 'p' and current_page > 0:
                        current_page -= 1
                    else:
                        break
            else:
                stdscr.addstr(4, 1, "No matches found.")
                stdscr.addstr(max_y - 1, 1, "Press any key to return.")
                stdscr.getch()
        elif choice == '4':
            break
        else:
            stdscr.addstr(max_y - 1, 1, "Invalid choice. Press any key to try again.")
            stdscr.getch()

curses.wrapper(main)