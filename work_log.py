"""
Work Log with a Database

Create entries by entering your name, date, title of task, time spent, and
optional notes to keep track of your timesheet information.  Employees can
search, edit, and delete existing entries.

This file handles the UI while work_log_db handles the database logic
"""
from collections import OrderedDict
from os import system, name
from textwrap import dedent
import datetime
import work_log_db


def clear_screen():
    """Clear the screen"""
    system('cls' if name == 'nt' else 'clear')


def get_employee_name():
    """Get the employee's full name and return it"""
    employee_name = ''
    while employee_name == '':
        employee_name = input('Please enter name: ')
        if employee_name != '':
            if len(employee_name) <= 50:
                clear_screen()
                return employee_name
            else:
                input('Must be 50 characters or less. Enter to continue')
                employee_name = ''
                clear_screen()
                continue
        else:
            input('An employee name must be entered.  Enter to continue')
            clear_screen()


def invalid_date_error(date_str):
    """Helper method for get_date() and get_2_dates(). Handles invalid dates"""
    print("Error: {} doesn't seem to be a valid date".format(date_str))
    input('Press enter to try again')
    clear_screen()


def get_date(optional_print_statement=None):
    """Gets a valid date from the user and returns it"""
    while True:
        if optional_print_statement:
            print(optional_print_statement)
        print('Date of the task')
        try:
            date_str = input('Please use YYYY/MM/DD: ')
            year, month, day = map(int, date_str.split('/'))

            # prevent a 2 digit year from being entered
            required_len_year = 4
            if len(str(year)) != required_len_year:
                invalid_date_error(date_str)
                continue

            date = datetime.date(year, month, day)
            clear_screen()
            return date
        except ValueError:
            invalid_date_error(date_str)
            continue


def get_task_name():
    """Gets a task_name from the user and returns it"""

    task_name = ''
    while task_name == '':
        task_name = input('Title of the task: ')
        if task_name != '':
            if len(task_name) <= 50:
                clear_screen()
                return task_name
            else:
                input('Must be 50 characters or less. Enter to continue')
                task_name = ''
                clear_screen()
                continue
        else:
            input('A task name must be entered.  Enter to continue')
            clear_screen()


def get_time_spent():
    """Gets a valid time spent from the user and returns it"""
    while True:
        try:
            time_spent = input('Time spent (rounded minutes): ')
            int(time_spent)
            clear_screen()
            if int(time_spent) <= 0:
                print('Time spent must be greater than zero')
                input('Press enter to try again')
                continue
            return time_spent
        except ValueError:
            error = "Error: {} doesn't seem to be a valid integer"
            print(error.format(time_spent))
            input('Press enter to try again')
            clear_screen()
            continue


def get_optional_notes():
    """Gets optional notes from the user and returns it"""
    optional_notes = input('Notes (Optional, you can leave this empty): ')
    clear_screen()
    return optional_notes


def get_2_dates():
    """
    Gets 2 valid dates from the user, with the first being <= to the second
    date, and returns the 2 dates
    """
    while True:
        print_statement = 'Enter the dates'
        date = get_date(print_statement)
        date_2 = get_date(print_statement)

        if date > date_2:
            error = "Error: {} is greater than {}"
            print(error.format(date, date_2))
            input('Press enter to try again')
            clear_screen()
            continue
        return date, date_2


def get_exact_string():
    """Gets and returns an exact text string"""
    print('Search by string in the task name or optional notes')
    exact_string = input('String: ')
    return exact_string


def get_list_of(filter_by, search_results):
    """Present user with a list of items which narrows the search
    This is used for the date_range_search and employee_name_search
    """
    # for each entry in the list, print a unique list
    item_set = set()
    item_dict = OrderedDict()
    matches = []
    entry_number = 1

    # If search_results is [], return []
    if search_results == []:
        return matches

    # Create a unique set
    for entry in search_results:
        item_set.add(entry[filter_by])

    # Create numbered dictionary
    for item in sorted(item_set):
        item_dict[entry_number] = item
        entry_number += 1

    # Allow the user to select by item
    exit_loop = False
    while exit_loop is False:
        try:
            print('Select one of the following: ')
            for key, value in item_dict.items():
                print('{}) {}'.format(key, value))
            choice = input('>').lower().strip()
            choice = item_dict[int(choice)]
            exit_loop = True
        except ValueError:
            print('Enter a valid integer choice from the list')
            input('Enter to continue')
            clear_screen()

    # Return the list
    for entry in search_results:
        if choice == entry[filter_by]:
            matches.append(entry)
    return matches


def add_entry():
    """Add new entry"""
    employee_name = get_employee_name()
    date = get_date()
    task_name = get_task_name()
    time_spent = get_time_spent()
    optional_notes = get_optional_notes()

    save = None

    while save != 'y':
        save = input('Save entry? [Yn] ').lower()

        if save == 'y':
            log_entry = {
                "employee_name": employee_name,
                "date": date,
                "task_name": task_name,
                "time_spent": time_spent,
                "optional_notes": optional_notes
            }
            entry = work_log_db.add_entry(log_entry)
            input('Entry added. Enter to return to the menu')
            return entry
        elif save == 'n':
            input('Entry not saved. Enter to continue')
            log_entry = {}
            return log_entry
        else:
            input("Enter a valid choice 'y' or 'n'. Enter to continue")
            clear_screen()
            continue


def search_menu_loop():
    """Search existing entries"""
    choice = None

    while choice != 'f':
        clear_screen()
        print(dedent("""\
            Do you want to search by:\
        """))
        for key, value in search_menu.items():
            print('{}) {}'.format(key, value.__doc__))

        choice = input('>').lower().strip()
        if choice in search_menu:
            clear_screen()
            search_menu[choice]()
        else:
            input('Enter a valid choice a-f. Enter to continue')


def quit():
    """Quit the program"""
    print(dedent("""\
                Thanks for using the Work Log program!
                Come again soon.\
            """))


def exact_date_search():
    """Exact date"""
    clear_screen()
    date = get_date()
    matches = work_log_db.exact_date_search(date)
    search_navigator(matches, count=0)


def date_range_search():
    """Range of dates"""
    clear_screen()
    date, date_2 = get_2_dates()
    matches = work_log_db.date_range_search(date, date_2)
    matches = get_list_of('date', matches)
    search_navigator(matches, count=0)


def time_spent_search():
    """Time spent"""
    clear_screen()
    time_spent = get_time_spent()
    matches = work_log_db.time_spent_search(time_spent)
    search_navigator(matches, count=0)


def exact_search():
    """Exact search"""
    clear_screen()
    exact_string = get_exact_string()
    matches = work_log_db.exact_search(exact_string)
    search_navigator(matches, count=0)


def employee_name_search():
    """Employee name"""
    clear_screen()
    employee_name = get_employee_name()
    matches = work_log_db.employee_name_search(employee_name)
    matches = get_list_of('employee_name', matches)
    search_navigator(matches, count=0)


def quit_search():
    """Return to menu"""
    # The quit_search function is complete and the pass below is intentional
    pass


def main_menu_loop():
    """Display main menu"""
    choice = None

    while choice != 'c':
        clear_screen()
        print(dedent("""\
            WORK LOG
            What would you like to do?\
        """))
        for key, value in main_menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('>').lower().strip()

        if choice in main_menu:
            clear_screen()
            main_menu[choice]()
        else:
            input("Please enter 'a', 'b', or 'c'\nEnter to continue")


def print_navigator_template(navigator_template, list, count, template):
    """Helper function for search_navigator. Prints navigator template"""
    print(navigator_template.format(
            list[count]["employee_name"], list[count]["date"],
            list[count]["task_name"], list[count]["time_spent"],
            list[count]["optional_notes"], count+1, len(list)
            ), template, sep='')


def edit_entry(list, count):
    """Helper function for search_navigator. Edits entry"""
    clear_screen()

    employee_name = get_employee_name()
    date = get_date()
    task_name = get_task_name()
    time_spent = get_time_spent()
    optional_notes = get_optional_notes()

    save = None

    while save != 'y':
        save = input('Save entry? [Yn] ').lower()

        if save == 'y':
            modification = {
                'employee_name': employee_name,
                'date': date,
                'task_name': task_name,
                'time_spent': time_spent,
                'optional_notes': optional_notes
            }
            original_entry = dict(list[count])
            modification = work_log_db.edit_entry(original_entry, modification)

            for item in modification:
                list[count]['{}'.format(item)] = modification[
                    '{}'.format(item)]

            input('The entry has been edited. Press enter')
            return list
        elif save == 'n':
            input('Entry not saved')
            return list
        else:
            input("Enter a valid choice 'y' or 'n'. Enter to continue")
            clear_screen()
            continue


def delete_entry(list, count):
    """Helper function for search_navigator.  Deletes entry."""
    delete = None

    while delete != 'y':
        clear_screen()
        delete = input('Delete entry? [Yn] ').lower()

        if delete == 'y':
            work_log_db.delete_entry(dict(list[count]))
            del list[count]
            input('The entry has been deleted. Press enter')
            return list
        elif delete == 'n':
            input('Entry not deleted')
            return list
        else:
            input("Enter a valid choice 'y' or 'n'. Enter to continue")
            continue


def search_navigator(list, count):
    """
    Allows the user to navigate through entries found, edit entries,
    delete entries, and to return to the search menu
    """
    clear_screen()

    navigator_template = dedent("""\
        Employee Name: {},
        Date: {},
        Title: {},
        Time Spent: {},
        Notes: {},\n
        Result {} of {}\n
    """)

    e_d_r_template = '[E]dit, [D]elete, [R]eturn to search menu'
    n_e_d_r_template = '[N]ext, [E]dit, [D]elete, [R]eturn to search menu'
    p_e_d_r_template = '[P]revious, [E]dit, [D]elete, [R]eturn to search menu'
    n_p_e_d_r_template = dedent("""\
        [N]ext, [P]revious, [E]dit, [D]elete, [R]eturn to search menu\
    """)

    # List is length 0 - there are no matches found or left
    if len(list) == 0:
        no_matches = 'No matches found\nPress enter to continue'
        input(no_matches)
        clear_screen()
    # List is length 1 - there is 1 match found or left
    elif len(list) == 1:
        is_valid = False
        while is_valid is False:
            print_navigator_template(
                navigator_template,
                list, count,
                e_d_r_template
            )

            choice = input('>')

            if choice.lower() == 'e':
                is_valid = True
                list = edit_entry(list, count)
                search_navigator(list, count)
                clear_screen()
            elif choice.lower() == 'd':
                is_valid = True
                list = delete_entry(list, count)
                search_navigator(list, count)
                clear_screen()
            elif choice.lower() == 'r':
                is_valid = True
                clear_screen()
            else:
                error = dedent("""\
                Please enter 'e', 'd' or 'r'
                Enter to continue""")
                input(error)
                clear_screen()
    # The list has 2 or more entries and this is the first list item
    elif count == 0:
        is_valid = False
        while is_valid is False:
            print_navigator_template(
                navigator_template,
                list,
                count,
                n_e_d_r_template
            )

            choice = input('>')

            if choice.lower() == 'n':
                is_valid = True
                count += 1
                search_navigator(list, count)
            elif choice.lower() == 'e':
                is_valid = True
                list = edit_entry(list, count)
                search_navigator(list, count)
                clear_screen()
            elif choice.lower() == 'd':
                is_valid = True
                list = delete_entry(list, count)
                search_navigator(list, count)
                clear_screen()
            elif choice.lower() == 'r':
                is_valid = True
                clear_screen()
            else:
                error = dedent("""\
                Please enter 'n', 'e', 'd' or 'r'
                Enter to continue""")
                input(error)
                clear_screen()
    # This is the last item in the list
    elif count+1 == len(list):
        is_valid = False
        while is_valid is False:
            print_navigator_template(
                navigator_template,
                list,
                count,
                p_e_d_r_template
            )

            choice = input('>')

            if choice.lower() == 'p':
                is_valid = True
                count -= 1
                search_navigator(list, count)
            elif choice.lower() == 'e':
                is_valid = True
                list = edit_entry(list, count)
                search_navigator(list, count)
                clear_screen()
            elif choice.lower() == 'd':
                is_valid = True
                list = delete_entry(list, count)
                search_navigator(list, count-1)
                clear_screen()
            elif choice.lower() == 'r':
                is_valid = True
                clear_screen()
            else:
                error = dedent("""\
                Please enter 'p', 'e', 'd' or 'r'
                Enter to continue""")
                input(error)
                clear_screen()
    # List items between the first and last list items
    else:
        is_valid = False
        while is_valid is False:
            print_navigator_template(
                navigator_template,
                list,
                count,
                n_p_e_d_r_template
            )

            choice = input('>')

            if choice.lower() == 'n':
                is_valid = True
                count += 1
                search_navigator(list, count)
            elif choice.lower() == 'p':
                is_valid = True
                count -= 1
                search_navigator(list, count)
            elif choice.lower() == 'e':
                is_valid = True
                list = edit_entry(list, count)
                search_navigator(list, count)
                clear_screen()
            elif choice.lower() == 'd':
                is_valid = True
                list = delete_entry(list, count)
                search_navigator(list, count)
                clear_screen()
            elif choice.lower() == 'r':
                is_valid = True
                clear_screen()
            else:
                error = dedent("""\
                Please enter 'n', 'p', 'e', 'd' or 'r'
                Enter to continue""")
                input(error)
                clear_screen()


main_menu = OrderedDict([
        ('a', add_entry),
        ('b', search_menu_loop),
        ('c', quit),
    ])

search_menu = OrderedDict([
        ('a', exact_date_search),
        ('b', date_range_search),
        ('c', time_spent_search),
        ('d', exact_search),
        ('e', employee_name_search),
        ('f', quit_search),
    ])

if __name__ == '__main__':
    work_log_db.initialize()
    main_menu_loop()
