"""This file tests the work_log.py and work_log_db.py files"""
import datetime
import unittest
import work_log
import work_log_db
from unittest.mock import patch
from peewee import SqliteDatabase
from work_log_db import Entry


test_database = SqliteDatabase(':memory:')


class WorkLogUITests(unittest.TestCase):
    def setUp(self):
        test_database.bind([Entry], bind_refs=False, bind_backrefs=False)
        test_database.connect()
        test_database.create_tables([Entry], safe=True)

        # For first log entry
        self.employee_name = 'John Smith'
        self.date = datetime.date(2019, 3, 20)
        self.task_name = 'test add entry'
        self.time_spent = 5
        self.optional_notes = 'apples'

        self.log_entry = {
            "employee_name": self.employee_name,
            "date": self.date,
            "task_name": self.task_name,
            "time_spent": self.time_spent,
            "optional_notes": self.optional_notes
        }

        # For the 2nd log entry
        self.employee_name_new = 'Jane Rogers'
        self.date_new = datetime.date(2019, 2, 12)
        self.task_name_new = 'edited entry'
        self.time_spent_new = 10
        self.optional_notes_new = 'apples and grapes'

        self.new_log_entry = {
            "employee_name": self.employee_name_new,
            "date": self.date_new,
            "task_name": self.task_name_new,
            "time_spent": self.time_spent_new,
            "optional_notes": self.optional_notes_new
        }

        # log_entry_1 and log_entry_2 are used for test_exact_date_search
        # and test_time_spent_search
        self.employee_name_1 = 'John Smith'
        self.date_1 = datetime.date(2019, 3, 20)
        self.task_name_1 = 'entry'
        self.time_spent_1 = 5
        self.optional_notes_1 = 'apples'

        self.log_entry_1 = {
            "employee_name": self.employee_name_1,
            "date": self.date_1,
            "task_name": self.task_name_1,
            "time_spent": self.time_spent_1,
            "optional_notes": self.optional_notes_1
        }

        self.employee_name_2 = 'John Smith'
        self.date_2 = datetime.date(2019, 3, 20)
        self.task_name_2 = 'entry'
        self.time_spent_2 = 5
        self.optional_notes_2 = 'apples'

        self.log_entry_2 = {
            "employee_name": self.employee_name_2,
            "date": self.date_2,
            "task_name": self.task_name_2,
            "time_spent": self.time_spent_2,
            "optional_notes": self.optional_notes_2
        }

        # Log entries for date_range_search - have different dates
        # Date is 2019/3/1
        self.employee_name_dr_1 = 'John Smith'
        self.date_dr_1 = datetime.date(2019, 3, 1)
        self.task_name_dr_1 = 'entry'
        self.time_spent_dr_1 = 5
        self.optional_notes_dr_1 = 'apples'

        self.log_entry_dr_1 = {
            "employee_name": self.employee_name_dr_1,
            "date": self.date_dr_1,
            "task_name": self.task_name_dr_1,
            "time_spent": self.time_spent_dr_1,
            "optional_notes": self.optional_notes_dr_1
        }

        # Date is 2019/3/15
        self.employee_name_dr_2 = 'John Smith'
        self.date_dr_2 = datetime.date(2019, 3, 15)
        self.task_name_dr_2 = 'entry'
        self.time_spent_dr_2 = 5
        self.optional_notes_dr_2 = 'apples'

        self.log_entry_dr_2 = {
            "employee_name": self.employee_name_dr_2,
            "date": self.date_dr_2,
            "task_name": self.task_name_dr_2,
            "time_spent": self.time_spent_dr_2,
            "optional_notes": self.optional_notes_dr_2
        }

        # Date is 2019/4/3
        self.employee_name_dr_3 = 'John Smith'
        self.date_dr_3 = datetime.date(2019, 4, 3)
        self.task_name_dr_3 = 'entry'
        self.time_spent_dr_3 = 5
        self.optional_notes_dr_3 = 'apples'

        self.log_entry_dr_3 = {
            "employee_name": self.employee_name_dr_3,
            "date": self.date_dr_3,
            "task_name": self.task_name_dr_3,
            "time_spent": self.time_spent_dr_3,
            "optional_notes": self.optional_notes_dr_3
        }

        # Log entry 3, 4, and 5 are for test_get_list_of
        self.employee_name_3 = 'Larry Appleton'
        self.date_3 = datetime.date(2019, 4, 4)
        self.task_name_3 = 'log entry 3'
        self.time_spent_3 = 15
        self.optional_notes_3 = 'apples'

        self.log_entry_3 = {
            "employee_name": self.employee_name_3,
            "date": self.date_3,
            "task_name": self.task_name_3,
            "time_spent": self.time_spent_3,
            "optional_notes": self.optional_notes_3
        }

        # Log entry 3, 4, and 5 are for test_get_list_of
        self.employee_name_4 = 'Larry Appleton'
        self.date_4 = datetime.date(2019, 4, 3)
        self.task_name_4 = 'log entry 4'
        self.time_spent_4 = 15
        self.optional_notes_4 = 'apples x 2'

        self.log_entry_4 = {
            "employee_name": self.employee_name_4,
            "date": self.date_4,
            "task_name": self.task_name_4,
            "time_spent": self.time_spent_4,
            "optional_notes": self.optional_notes_4
        }

        # Log entry 3, 4, and 5 are for test_get_list_of
        self.employee_name_5 = 'Larry Apple'
        self.date_5 = datetime.date(2019, 4, 2)
        self.task_name_5 = 'log entry 5'
        self.time_spent_5 = 15
        self.optional_notes_5 = 'apple less'

        self.log_entry_5 = {
            "employee_name": self.employee_name_5,
            "date": self.date_5,
            "task_name": self.task_name_5,
            "time_spent": self.time_spent_5,
            "optional_notes": self.optional_notes_5
        }

    def test_add_entry(self):
        """Test add_entry from work_log_db.py"""
        # No entries in database

        # Query database
        result = Entry.select().where(
            Entry.employee_name == self.employee_name and
            Entry.date == self.date and
            Entry.task_name == self.task_name and
            Entry.time_spent == self.time_spent and
            Entry.optional_notes == self.optional_notes
        )

        # Check to see if in database
        if result.exists():
            result = True
        else:
            result = False

        # Assert no entries in the database
        self.assertFalse(result)

        # Add entry to database
        work_log_db.add_entry(self.log_entry)

        # Query database
        result = Entry.select().where(
            Entry.employee_name == self.employee_name and
            Entry.date == self.date and
            Entry.task_name == self.task_name and
            Entry.time_spent == self.time_spent and
            Entry.optional_notes == self.optional_notes
        )

        # Assert entry in database
        self.assertEqual(result[0].employee_name, self.employee_name)
        self.assertEqual(result[0].date, self.date)
        self.assertEqual(result[0].task_name, self.task_name)
        self.assertEqual(result[0].time_spent, self.time_spent)
        self.assertEqual(result[0].optional_notes, self.optional_notes)

    def test_delete_entry(self):
        """Test if entry has been deleted from the database"""
        # No entries in the database

        # Count number of entries in the database
        result = Entry.select().count()

        # Assert no entries
        self.assertEqual(result, 0)

        # Add entry to database
        work_log_db.add_entry(self.log_entry)

        # Count number of entries in the database
        result = Entry.select().count()

        # Assert there is 1 entry in the database
        self.assertEqual(result, 1)

        # Delete entry from database
        work_log_db.delete_entry(self.log_entry)

        # Count number of entries in the database
        result = Entry.select().count()

        # Assert no entries
        self.assertEqual(result, 0)

    def test_edit_entry(self):
        """Test entry to see if it's been edited in database"""
        # Add entry 1 to database and then edit it
        work_log_db.add_entry(self.log_entry)
        work_log_db.edit_entry(self.log_entry, self.new_log_entry)

        # Count number of entries in the database
        result = Entry.select().count()

        # Assert there is 1 entry in the database
        self.assertEqual(result, 1)

        # Query the edited entry from the database
        result = Entry.select().where(
            Entry.employee_name == self.employee_name_new and
            Entry.date == self.date_new and
            Entry.task_name == self.task_name_new and
            Entry.time_spent == self.time_spent_new and
            Entry.optional_notes == self.optional_notes_new
        )

        # Shows what's in the database is equal to the edited entry
        self.assertEqual(result[0].employee_name, self.employee_name_new)
        self.assertEqual(result[0].date, self.date_new)
        self.assertEqual(result[0].task_name, self.task_name_new)
        self.assertEqual(result[0].time_spent, self.time_spent_new)
        self.assertEqual(result[0].optional_notes, self.optional_notes_new)

    def test_exact_date_search(self):
        """Test exact date search"""
        # Add 2 log entries with the same date and one that differs by date
        work_log_db.add_entry(self.log_entry_1)
        work_log_db.add_entry(self.log_entry_2)
        work_log_db.add_entry(self.new_log_entry)  # This log entry differs

        # Query the database for entries with that date
        result = Entry.select().where(
            Entry.date == self.date_1
        )

        # Assert there are 2 entries with the date queried
        self.assertEqual(result.count(), 2)

        # Use exact_date_search
        search_result = work_log_db.exact_date_search(self.date_1)

        #  Assert count from database equals count from exact_date_search
        self.assertEqual(result.count(), len(search_result))

        # Entry 1 in database equals entry 1 from exact_date_search
        self.assertEqual(
            result[0].employee_name, search_result[0]["employee_name"])
        self.assertEqual(
            result[0].date, search_result[0]["date"])
        self.assertEqual(
            result[0].task_name, search_result[0]["task_name"])
        self.assertEqual(
            result[0].time_spent, search_result[0]["time_spent"])
        self.assertEqual(
            result[0].optional_notes, search_result[0]["optional_notes"])

        # Entry 2 in database equals entry 2 from exact_date_search
        self.assertEqual(
            result[1].employee_name, search_result[1]["employee_name"])
        self.assertEqual(
            result[1].date, search_result[1]["date"])
        self.assertEqual(
            result[1].task_name, search_result[1]["task_name"])
        self.assertEqual(
            result[1].time_spent, search_result[1]["time_spent"])
        self.assertEqual(
            result[1].optional_notes, search_result[1]["optional_notes"])

    def test_date_range_search(self):
        """Test date range search"""
        # No entries in database

        # Start and end date for the date range search
        date_1 = datetime.date(2019, 3, 1)
        date_2 = datetime.date(2019, 4, 3)

        # Query the database
        search_result = work_log_db.date_range_search(date_1, date_2)

        # Assert nothing returned back from the search
        self.assertEqual(search_result, [])

        # Add 3 entries with different dates but within the range
        work_log_db.add_entry(self.log_entry_dr_1)
        work_log_db.add_entry(self.log_entry_dr_2)
        work_log_db.add_entry(self.log_entry_dr_3)

        # Add 1 entry with a date outside of the search range
        work_log_db.add_entry(self.new_log_entry)

        # Query by database date range
        result = Entry.select().where(Entry.date.between(date_1, date_2))

        # Should return the 3 entries that are in the search range
        search_result = work_log_db.date_range_search(date_1, date_2)

        # Assert number of entries from search result equals number
        # added to database minus 1
        self.assertEqual(len(search_result), Entry.select().count()-1)

        # Assert first entry added (earliest date) equals last entry
        # from search result since results are returned in descending
        # order from the date_range_search
        self.assertEqual(
            result[0].employee_name, search_result[2]["employee_name"])
        self.assertEqual(
            result[0].date, search_result[2]["date"])
        self.assertEqual(
            result[0].task_name, search_result[2]["task_name"])
        self.assertEqual(
            result[0].time_spent, search_result[2]["time_spent"])
        self.assertEqual(
            result[0].optional_notes, search_result[2]["optional_notes"])

        # Assert 2nd entry added equals middle list item
        self.assertEqual(
            result[1].employee_name, search_result[1]["employee_name"])
        self.assertEqual(
            result[1].date, search_result[1]["date"])
        self.assertEqual(
            result[1].task_name, search_result[1]["task_name"])
        self.assertEqual(
            result[1].time_spent, search_result[1]["time_spent"])
        self.assertEqual(
            result[1].optional_notes, search_result[1]["optional_notes"])

        # Assert 3rd entry added equals first list item
        self.assertEqual(
            result[2].employee_name, search_result[0]["employee_name"])
        self.assertEqual(
            result[2].date, search_result[0]["date"])
        self.assertEqual(
            result[2].task_name, search_result[0]["task_name"])
        self.assertEqual(
            result[2].time_spent, search_result[0]["time_spent"])
        self.assertEqual(
            result[2].optional_notes, search_result[0]["optional_notes"])

    def test_time_spent_search(self):
        """Test time spent search"""
        # Nothing in database yet so search result should return []
        search_result = work_log_db.time_spent_search(5)
        self.assertEqual(search_result, [])

        # Add 2 entries with the same time_spent and one with a
        # different time spent
        work_log_db.add_entry(self.log_entry_1)
        work_log_db.add_entry(self.log_entry_2)
        work_log_db.add_entry(self.new_log_entry)  # Has different time spent

        # Query database
        search_result = work_log_db.time_spent_search(5)

        # Assert that length of search result equals count from database
        result = Entry.select().where(
            Entry.time_spent == self.time_spent_1).count()
        self.assertEqual(len(search_result), result)

        # Assert that length of search result equals 2
        self.assertEqual(len(search_result), 2)

        # Returns entries where time_spent is 5
        result = Entry.select().where(
            Entry.time_spent == self.time_spent_1)

        # First entry added should equal search result's first entry
        self.assertEqual(
            result[0].employee_name, search_result[0]["employee_name"])
        self.assertEqual(
            result[0].date, search_result[0]["date"])
        self.assertEqual(
            result[0].task_name, search_result[0]["task_name"])
        self.assertEqual(
            result[0].time_spent, search_result[0]["time_spent"])
        self.assertEqual(
            result[0].optional_notes, search_result[0]["optional_notes"])

        # Second entry added should equal search result's second entry
        self.assertEqual(
            result[1].employee_name, search_result[1]["employee_name"])
        self.assertEqual(
            result[1].date, search_result[1]["date"])
        self.assertEqual(
            result[1].task_name, search_result[1]["task_name"])
        self.assertEqual(
            result[1].time_spent, search_result[1]["time_spent"])
        self.assertEqual(
            result[1].optional_notes, search_result[1]["optional_notes"])

    def test_exact_search(self):
        """Test exact search"""
        # Nothing added to database yet.  Search should return []
        search_result = work_log_db.exact_search('add')
        self.assertEqual(search_result, [])

        # Nothing added to database yet.  Search should return []
        search_result = work_log_db.exact_search('app')
        self.assertEqual(search_result, [])

        # Add entry to database
        work_log_db.add_entry(self.log_entry)

        # Entry contains word "add" in the task name
        search_result = work_log_db.exact_search('add')
        self.assertNotEqual(search_result, [])

        # Optional notes contain "apples"
        search_result = work_log_db.exact_search('app')
        self.assertNotEqual(search_result, [])

        # Returns entry that was added to the database
        result = Entry.select().where(
            Entry.employee_name == self.employee_name and
            Entry.date == self.date and
            Entry.task_name == self.task_name and
            Entry.time_spent == self.time_spent and
            Entry.optional_notes == self.optional_notes
        )

        # Entry added should equal search_result
        self.assertEqual(
            result[0].employee_name, search_result[0]["employee_name"])
        self.assertEqual(
            result[0].date, search_result[0]["date"])
        self.assertEqual(
            result[0].task_name, search_result[0]["task_name"])
        self.assertEqual(
            result[0].time_spent, search_result[0]["time_spent"])
        self.assertEqual(
            result[0].optional_notes, search_result[0]["optional_notes"])

    def test_employee_name_search(self):
        """Test employee name search"""
        # Nothing added to database yet
        search_result = work_log_db.employee_name_search('John Smith')
        self.assertEqual(search_result, [])

        # Add entry to database
        work_log_db.add_entry(self.log_entry)  # 2019/3/20

        # Search by name
        search_result = work_log_db.employee_name_search('John Smith')

        # Assert search result is not []
        self.assertNotEqual(search_result, [])

        # Query entry from database
        result = Entry.select().where(
            Entry.employee_name == self.employee_name and
            Entry.date == self.date and
            Entry.task_name == self.task_name and
            Entry.time_spent == self.time_spent and
            Entry.optional_notes == self.optional_notes
        )

        # Entry added should equal search_result
        self.assertEqual(
            result[0].employee_name, search_result[0]["employee_name"])
        self.assertEqual(
            result[0].date, search_result[0]["date"])
        self.assertEqual(
            result[0].task_name, search_result[0]["task_name"])
        self.assertEqual(
            result[0].time_spent, search_result[0]["time_spent"])
        self.assertEqual(
            result[0].optional_notes, search_result[0]["optional_notes"])

        # Add another entry to database with a different date but
        # with the same name
        # Entries are returned back in descending order by date
        work_log_db.add_entry(self.log_entry_dr_3)  # 2019/4/3

        # Search by name
        search_result = work_log_db.employee_name_search('John Smith')

        # Query log_entry_dr_3
        result = Entry.select().where(
            Entry.date == self.date_dr_3)

        # Entry added should be first in search results
        self.assertEqual(
            result[0].employee_name, search_result[0]["employee_name"])
        self.assertEqual(
            result[0].date, search_result[0]["date"])
        self.assertEqual(
            result[0].task_name, search_result[0]["task_name"])
        self.assertEqual(
            result[0].time_spent, search_result[0]["time_spent"])
        self.assertEqual(
            result[0].optional_notes, search_result[0]["optional_notes"])

    # Above was work_log_db.py testing and below is work_log.py testing
    # All methods that end in ui are testing the ui

    def test_get_employee_name_ui(self):
        """Test get_employee_name function"""
        input_args = [
            '',  # enter invalid name
            '',  # enter to continue - below name is over 50 characters
            '012345678901234567890123456789012345678901234567890123456789',
            '',  # enter to continue
            self.employee_name,  # valid employee name
        ]

        with patch('builtins.input', side_effect=input_args) as mock:
            work_log.get_employee_name()

    def test_invalid_date_error_ui(self):
        """Test invalid_date_error function"""
        input_args = [
            '',  # enter to continue
        ]

        with patch('builtins.input', side_effect=input_args) as mock:
            work_log.invalid_date_error('19/4/2')

    def test_get_date_ui(self):
        """Test get_date function"""
        input_args = [
            '',  # enter invalid date
            '',  # enter to continue
            '19/4/3',  # enter invalid date - year must be 4 digits
            '',  # enter to continue
            '2019/4/3',  # valid date entered
        ]

        with patch('builtins.input', side_effect=input_args) as mock:
            work_log.get_date('Enter the dates')

    def test_get_task_name_ui(self):
        """Test get_task_name function"""
        input_args = [
            '',  # enter invalid task name
            '',  # enter to continue - below is over 50 characters
            '012345678901234567890123456789012345678901234567890123456789',
            '',  # enter to continue
            'task entry',  # valid task name
        ]

        with patch('builtins.input', side_effect=input_args) as mock:
            work_log.get_task_name()

    def test_get_time_spent_ui(self):
        """Test get_time_spent function"""
        input_args = [
            '1.1',  # enter invalid time_spent which must be integer
            '',  # enter to continue - below is over 50 characters
            '0',  # enter invalid time_spent - must be greater than 0
            '',  # enter to continue
            '5',  # valid time spent
        ]

        with patch('builtins.input', side_effect=input_args) as mock:
            work_log.get_time_spent()

    def test_get_optional_notes_ui(self):
        """Test get_optional_notes function"""
        input_args = [
            '',  # entered nothing for optional note
        ]

        with patch('builtins.input', side_effect=input_args) as mock:
            work_log.get_optional_notes()

    def test_get_2_dates_ui(self):
        """Test get_2_dates function"""
        input_args = [
            '2019/4/4',  # date 1 greater than date 2
            '2019/4/1',  # date 2 less then date 1 - will produce error
            '',  # enter to continue
            '2019/4/1',  # date 1 less than date 2
            '2019/4/4',  # date 2 greater than date 1
        ]

        with patch('builtins.input', side_effect=input_args) as mock:
            work_log.get_2_dates()

    def test_get_exact_string_ui(self):
        """Test get_exact_string function"""
        input_args = [
            'my search',  # enter a string
        ]

        with patch('builtins.input', side_effect=input_args) as mock:
            work_log.get_exact_string()

    def test_get_list_of_ui(self):
        """Test get_list_of function"""
        # Test when matches input into get_list_of is []
        input_args = []

        with patch('builtins.input', side_effect=input_args) as mock:
            matches = []
            result = work_log.get_list_of('employee_name', matches)

            # Assert that get_list_of returns []
            self.assertEqual(result, [])

            # Test with matches present
            input_args = [
                'q',  # invalid input - choices are 1 or 2
                '',  # enter to continue
                '2',  # enter valid choice
            ]

            with patch('builtins.input', side_effect=input_args) as mock:
                matches = [
                    self.log_entry_3,
                    self.log_entry_4,
                    self.log_entry_5,
                ]
                # Will only have entries for Larry Appleton which
                # are log entry 3 and 4
                result = work_log.get_list_of('employee_name', matches)

                # Assert first entry in result equals log entry 3
                self.assertEqual(result[0], self.log_entry_3)

                # Assert second entry equals log entry 4
                self.assertEqual(result[1], self.log_entry_4)

    def test_add_entry_ui(self):
        """Test add_entry in work_log.py - the ui"""
        # Testing add entry but not saving
        input_args = [
            self.employee_name,  # enter employee name
            '2019/3/20',  # enter date
            self.task_name,  # enter task name
            self.time_spent,  # enter time spent
            self.optional_notes,  # enter optional notes
            'q',  # invalid choice for save entry [Yn]
            '',  # enter to continue
            'n',  # not saving entry
            '',  # enter to continue
        ]

        with patch('builtins.input', side_effect=input_args) as mock:
            result = work_log.add_entry()

            # Assert that result equals {}
            self.assertEqual(result, {})

            input_args = [
                self.employee_name,  # enter employee name
                '2019/3/20',  # enter date
                self.task_name,  # enter task name
                self.time_spent,  # enter time spent
                self.optional_notes,  # enter optional notes
                'y',  # to save
                '',  # enter to continue
            ]
            with patch('builtins.input', side_effect=input_args) as mock:
                result = work_log.add_entry()
                self.assertEqual(result, self.log_entry)

    def test_edit_entry_ui(self):
        """Test edit_entry in work_log.py - the ui"""
        # Testing edited entry that is not saved
        input_args = [
            "Jill Peterson",  # enter employee name
            '2019/4/4',  # enter date
            'edited task',  # enter task name
            '30',  # enter time spent
            'optional note',  # enter optional note
            'q',  # enter invalid input
            '',  # enter to continue
            'n',  # to not save
            '',  # enter to continue
        ]

        with patch('builtins.input', side_effect=input_args) as mock:
            entry_list = [
                self.log_entry,
                self.new_log_entry,
            ]
            result = work_log.edit_entry(entry_list, count=0)

            # Since entry not saved, asserting result equals []
            # This shows the entry has not been edited
            self.assertEqual(result, entry_list)

            # Testing edited entry that is saved
            input_args = [
                "Jill Peterson",  # enter employee name
                '2019/4/4',  # enter date
                'edited task',  # enter task name
                '30',  # enter time spent
                'optional note',  # enter optional note
                'y',  # to save
                '',  # enter to continue
            ]

            with patch('builtins.input', side_effect=input_args) as mock:
                entry_list = [
                    self.log_entry,
                    self.new_log_entry,
                ]
                result = work_log.edit_entry(entry_list, count=0)

                log_entry_for_edit = {
                    'employee_name': 'Jill Peterson',
                    'date': datetime.date(2019, 4, 4),
                    'task_name': 'edited task',
                    'time_spent': '30',
                    'optional_notes': 'optional note',
                }

                # Assert entry in result equals log_entry_for_edit
                self.assertEqual(result[0], log_entry_for_edit)

    def test_delete_entry_ui(self):
        """Test delete_entry in work_log.py - in the ui"""
        # Test delete_entry and choose to not delete
        input_args = [
            'q',  # enter invalid input - 'y' or 'n' required
            '',  # enter to continue
            'n',  # not to delete
            '',  # enter to continue
        ]

        with patch('builtins.input', side_effect=input_args) as mock:
            item_to_delete = [
                self.log_entry
            ]

            result = work_log.delete_entry(item_to_delete, count=0)

            # Assert item in result is equal to item in item_to_delete
            self.assertEqual(result, item_to_delete)

            input_args = [
                'y',  # enter 'y' to delete
                '',  # enter to continue
            ]

            with patch('builtins.input', side_effect=input_args) as mock:
                item_to_delete = [
                    self.log_entry
                ]

                result = work_log.delete_entry(item_to_delete, count=0)

                # Assert delete_entry returns []
                self.assertEqual(result, [])

    # The below is integration testing

    def test_integration_test_1(self):
        """Test main menu loop, search menu loop, exact date search,
        date range search, time spent search, exact search,
        employee name search, quit search, and quit.
        """
        input_args = [
            'q',  # invalid input
            '',  # enter to continue
            'b',  # to enter search menu loop
            'q',  # invalid input
            '',  # enter to continue
            'a',  # for exact date search
            '2019/4/2',  # enter date
            '',  # enter to continue
            'b',  # date range search
            '2019/4/2',  # enter date 1
            '2019/4/4',  # enter date 2
            '',  # enter to continue
            'c',  # time spent search
            '5',  # enter time spent
            '',  # enter to continue
            'd',  # exact search
            'exact string',  # exact string
            '',  # enter to continue
            'e',  # employee name search
            'John Smith',  # enter employee name
            '',  # enter to continue
            'f',  # quit search
            'c',  # quit program
        ]

        with patch('builtins.input', side_effect=input_args) as mock:
            work_log.main_menu_loop()

    def test_search_navigator_list_1_and_0(self):
        """Test search_navigator for lists of length 1 and 0"""
        # Add entry to database so lists of length 1 and 0 can be tested
        work_log_db.add_entry(self.log_entry)

        input_args = [
            'b',  # enter search menu
            'a',  # exact date search
            '2019/3/20',  # enter date to search by
            'q',  # invalid input
            '',  # enter to continue
            'r',  # return to search menu
            'a',  # exact date search
            '2019/3/20',  # enter date to search by
            'e',  # edit entry
            self.employee_name_new,  # enter employee name
            '2019/2/12',  # enter date
            self.task_name_new,  # enter task name
            self.time_spent_new,  # enter time spent
            self.optional_notes_new,  # enter optional notes
            'n',  # not to save
            '',  # enter to continue
            'd',  # delete entry
            'y',  # confirm deletion
            '',  # enter to continue
            '',  # enter to continue
            'f',  # quit search
            'c',  # quit program
        ]

        with patch('builtins.input', side_effect=input_args) as mock:
            work_log.main_menu_loop()

    def test_search_navigator_2_item_list_1st(self):
        """Test search_navigator for lists of length 2 or greater
        and it's the first item in the list
        """
        # Add 2 entries to the database
        work_log_db.add_entry(self.log_entry_1)
        work_log_db.add_entry(self.log_entry_2)

        input_args = [
            'b',  # enter search menu
            'a',  # exact date search
            '2019/3/20',  # enter date to search by
            'q',  # invalid input
            '',  # enter to continue
            'n',  # next
            'p',  # return to target entry
            'r',  # return to search menu
            'a',  # exact date search
            '2019/3/20',  # enter date to search by
            'e',  # edit entry
            self.employee_name_new,  # enter employee name
            '2019/2/12',  # enter date
            self.task_name_new,  # enter task name
            self.time_spent_new,  # enter time spent
            self.optional_notes_new,  # enter optional notes
            'n',  # not to save
            '',  # enter to continue
            'd',  # delete entry
            'y',  # confirm deletion
            '',  # enter to continue
            'r',  # return to search menu
            'f',  # quit search
            'c',  # quit program
        ]

        with patch('builtins.input', side_effect=input_args) as mock:
            work_log.main_menu_loop()

    def test_search_navigator_last_item_in_list(self):
        """Test last item in list and test employee name search"""
        # Add 2 entries to the database
        work_log_db.add_entry(self.log_entry_1)
        work_log_db.add_entry(self.log_entry_2)

        input_args = [
            'b',  # enter search menu
            'a',  # exact date search
            '2019/3/20',  # enter date to search by
            'n',  # proceed to target item
            'q',  # invalid input
            '',  # enter to continue
            'p',  # previous entry
            'n',  # return to target item
            'r',  # return to search menu
            'a',  # exact date search
            '2019/3/20',  # enter date to search by
            'n',  # proceed to target item
            'e',  # edit entry
            self.employee_name_new,  # enter employee name
            '2019/2/12',  # enter date
            self.task_name_new,  # enter task name
            self.time_spent_new,  # enter time spent
            self.optional_notes_new,  # enter optional notes
            'n',  # not to save
            '',  # enter to continue
            'd',  # delete entry
            'y',  # confirm deletion
            '',  # enter to continue
            'r',  # return to search menu
            'f',  # quit search
            'c',  # quit program
        ]

        with patch('builtins.input', side_effect=input_args) as mock:
            work_log.main_menu_loop()

    def test_search_navigator_list_item_in_middle(self):
        """Test when the item in the list is one of the middle items
        in the list
        """
        # Add 3 entries to the database
        work_log_db.add_entry(self.log_entry_1)
        work_log_db.add_entry(self.log_entry_2)
        work_log_db.add_entry(self.log_entry_3)

        input_args = [
            'b',  # enter search menu
            'd',  # exact search
            'entry',  # all 3 entries contain the word entry
            'n',  # advance to target item
            'q',  # invalid input
            '',  # enter to continue
            'n',  # next
            'p',  # return to target entry
            'p',  # previous
            'n',  # return to target entry
            'r',  # return to search menu
            'd',  # exact search
            'entry',  # all 3 entries contain the word entry
            'n',  # advance to target item
            'e',  # edit entry
            self.employee_name_new,  # enter employee name
            '2019/2/12',  # enter date
            self.task_name_new,  # enter task name
            self.time_spent_new,  # enter time spent
            self.optional_notes_new,  # enter optional notes
            'n',  # not to save
            '',  # enter to continue
            'd',  # delete entry
            'y',  # confirm deletion
            '',  # enter to continue
            'r',  # return to search menu
            'f',  # quit search
            'c',  # quit program
        ]

        with patch('builtins.input', side_effect=input_args) as mock:
            work_log.main_menu_loop()

    def tearDown(self):
        test_database.drop_tables([Entry])
        test_database.close()


if __name__ == '__main__':
    unittest.main()
