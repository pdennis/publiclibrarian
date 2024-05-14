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

def search_books_by_category(search_term):
    try:
        with open(LIBRARY_CSV, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            matches = [row for row in reader if search_term.lower() in row['LCSH'].lower()]
            return matches
    except FileNotFoundError:
        return None

def display_search_results(stdscr, results, current_page, scroll_pos):
    max_y, max_x = stdscr.getmaxyx()
    result_lines = []

    if current_page < len(results):
        result = results[current_page]
        title = f"Title: {result['Book title']}"
        author = f"Author: {result['Book Author']}"
        description = f"Description: {result['Book Description']}"
        category = f"Category: {result['LCSH']}"

        # Wrap long lines of text
        wrapped_title = textwrap.fill(title, width=max_x - 4)
        wrapped_author = textwrap.fill(author, width=max_x - 4)
        wrapped_description = textwrap.fill(description, width=max_x - 4)
        wrapped_category = textwrap.fill(category, width=max_x - 4)

        result_lines.extend(wrapped_title.split('\n'))
        result_lines.extend([''] + wrapped_author.split('\n'))
        result_lines.extend([''] + wrapped_description.split('\n'))
        result_lines.extend([''] + wrapped_category.split('\n'))

    # Calculate the available lines for displaying results
    available_lines = max_y - 8

    # Adjust the scroll position if necessary
    if scroll_pos > len(result_lines) - available_lines:
        scroll_pos = max(0, len(result_lines) - available_lines)

    # Display the visible portion of the result lines
    for i in range(available_lines):
        if scroll_pos + i < len(result_lines):
            stdscr.addstr(4 + i, 2, result_lines[scroll_pos + i])

    page_info = f"Page {current_page + 1} of {len(results)}"
    stdscr.addstr(max_y - 3, (max_x - len(page_info)) // 2, page_info)

    scroll_info = f"Line {scroll_pos + 1} of {len(result_lines)}"
    stdscr.addstr(max_y - 2, (max_x - len(scroll_info)) // 2, scroll_info)

    if current_page < len(results) - 1:
        stdscr.addstr(max_y - 3, 1, "Press 'n' for next page, 'p' for previous page,")
        stdscr.addstr(max_y - 2, 1, "'u' to scroll up, 'd' to scroll down,")
        stdscr.addstr(max_y - 1, 1, "or any other key to return.")
    else:
        stdscr.addstr(max_y - 2, 1, "Press 'p' for previous page, 'u' to scroll up,")
        stdscr.addstr(max_y - 1, 1, "'d' to scroll down, or any other key to return.")

    return scroll_pos

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

        menu_items = ["Search by title", "Search by author", "Search by description", "Search by category", "Exit"]
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
                scroll_pos = 0  # Initialize scroll position
                while True:
                    stdscr.clear()
                    scroll_pos = display_search_results(stdscr, results, current_page, scroll_pos)
                    stdscr.refresh()
                    key = stdscr.getkey()
                    if key == 'n' and current_page < len(results) - 1:
                        current_page += 1
                        scroll_pos = 0
                    elif key == 'p' and current_page > 0:
                        current_page -= 1
                        scroll_pos = 0
                    elif key == 'u':
                        scroll_pos = max(0, scroll_pos - 1)
                    elif key == 'd':
                        scroll_pos = display_search_results(stdscr, results, current_page, scroll_pos + 1)
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
            curses.echo()  # Enable echoing of typed characters
            search_term = stdscr.getstr(2, 1, 20).decode().strip()
            curses.noecho()  # Disable echoing of typed characters
            results = search_books_by_author(search_term)
            if results is None:
                stdscr.addstr(4, 1, "Error: Could not open library CSV file.")
            elif results:
                current_page = 0
                scroll_pos = 0  # Initialize scroll position
                while True:
                    stdscr.clear()
                    scroll_pos = display_search_results(stdscr, results, current_page, scroll_pos)
                    stdscr.refresh()
                    key = stdscr.getkey()
                    if key == 'n' and current_page < len(results) - 1:
                        current_page += 1
                        scroll_pos = 0
                    elif key == 'p' and current_page > 0:
                        current_page -= 1
                        scroll_pos = 0
                    elif key == 'u':
                        scroll_pos = max(0, scroll_pos - 1)
                    elif key == 'd':
                        scroll_pos = display_search_results(stdscr, results, current_page, scroll_pos + 1)
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
                scroll_pos = 0  # Initialize scroll position
                while True:
                    stdscr.clear()
                    scroll_pos = display_search_results(stdscr, results, current_page, scroll_pos)
                    stdscr.refresh()
                    key = stdscr.getkey()
                    if key == 'n' and current_page < len(results) - 1:
                        current_page += 1
                        scroll_pos = 0
                    elif key == 'p' and current_page > 0:
                        current_page -= 1
                        scroll_pos = 0
                    elif key == 'u':
                        scroll_pos = max(0, scroll_pos - 1)
                    elif key == 'd':
                        scroll_pos = display_search_results(stdscr, results, current_page, scroll_pos + 1)
                    else:
                        break
            else:
                stdscr.addstr(4, 1, "No matches found.")
                stdscr.addstr(max_y - 1, 1, "Press any key to return.")
                stdscr.getch()
        elif choice == '4':
            stdscr.clear()
            stdscr.addstr(1, 1, "Enter search term for book categories:")
            stdscr.refresh()
            curses.echo()  # Enable echoing of typed characters
            search_term = stdscr.getstr(2, 1, 20).decode().strip()
            curses.noecho()  # Disable echoing of typed characters
            results = search_books_by_category(search_term)
            if results is None:
                stdscr.addstr(4, 1, "Error: Could not open library CSV file.")
            elif results:
                current_page = 0
                scroll_pos = 0  # Initialize scroll position
                while True:
                    stdscr.clear()
                    scroll_pos = display_search_results(stdscr, results, current_page, scroll_pos)
                    stdscr.refresh()
                    key = stdscr.getkey()
                    if key == 'n' and current_page < len(results) - 1:
                        current_page += 1
                        scroll_pos = 0
                    elif key == 'p' and current_page > 0:
                        current_page -= 1
                        scroll_pos = 0
                    elif key == 'u':
                        scroll_pos = max(0, scroll_pos - 1)
                    elif key == 'd':
                        scroll_pos = display_search_results(stdscr, results, current_page, scroll_pos + 1)
                    else:
                        break
            else:
                stdscr.addstr(4, 1, "No matches found.")
                stdscr.addstr(max_y - 1, 1, "Press any key to return.")
                stdscr.getch()
        elif choice == '5':
            break
        else:
            stdscr.addstr(max_y - 1, 1, "Invalid choice. Press any key to try again.")
            stdscr.getch()

curses.wrapper(main)
