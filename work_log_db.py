"""This file handles the database logic for work_log.py"""
from peewee import *

db = SqliteDatabase('work_log.db')


class Entry(Model):
    employee_name = CharField(max_length=50)
    date = DateField()
    task_name = CharField(max_length=50)
    time_spent = IntegerField(default=0)
    optional_notes = TextField()

    class Meta:
        database = db


def initialize():
    """Create the database and table if they don't exist"""
    db.connect()
    db.create_tables([Entry], safe=True)


def add_entry(log_entry):
    """Add entry to database"""
    if log_entry:
        Entry.create(
            employee_name=log_entry['employee_name'],
            date=log_entry['date'],
            task_name=log_entry['task_name'],
            time_spent=log_entry['time_spent'],
            optional_notes=log_entry['optional_notes']
        )
        return log_entry


def delete_entry(entry):
    """Delete entry from database"""

    employee_name = entry['employee_name']
    date = entry['date']
    task_name = entry['task_name']
    time_spent = entry['time_spent']
    optional_notes = entry['optional_notes']

    entries = Entry.select().where(
        Entry.employee_name == employee_name and
        Entry.date == date and
        Entry.task_name == task_name and
        Entry.time_spent == time_spent and
        Entry.optional_notes == optional_notes
    )

    for entry in entries:
        entry.delete_instance()

    return entry


def edit_entry(old_entry, new_entry):
    """Edit entry in database"""
    employee_name = old_entry['employee_name']
    date = old_entry['date']
    task_name = old_entry['task_name']
    time_spent = old_entry['time_spent']
    optional_notes = old_entry['optional_notes']

    new_employee_name = new_entry['employee_name']
    new_date = new_entry['date']
    new_task_name = new_entry['task_name']
    new_time_spent = new_entry['time_spent']
    new_optional_notes = new_entry['optional_notes']

    entries = Entry.select().where(
        Entry.employee_name == employee_name and
        Entry.date == date and
        Entry.task_name == task_name and
        Entry.time_spent == time_spent and
        Entry.optional_notes == optional_notes
    )

    for entry in entries:
        entry.employee_name = new_employee_name
        entry.date = new_date
        entry.task_name = new_task_name
        entry.time_spent = new_time_spent
        entry.optional_notes = new_optional_notes
        entry.save()

    return new_entry


def exact_date_search(date):
    """Search database by exact date"""
    entries = Entry.select().where(Entry.date.contains(date))
    matches = []
    for entry in entries:
        matches.append({
                'employee_name': entry.employee_name,
                'date': entry.date,
                'task_name': entry.task_name,
                'time_spent': entry.time_spent,
                'optional_notes': entry.optional_notes
            })
    return matches


def date_range_search(date, date_2):
    """Search database by range of dates"""
    entries = Entry.select().where(
        Entry.date.between(date, date_2)).order_by(Entry.date.desc())
    matches = []
    for entry in entries:
        matches.append({
                'employee_name': entry.employee_name,
                'date': entry.date,
                'task_name': entry.task_name,
                'time_spent': entry.time_spent,
                'optional_notes': entry.optional_notes
            })
    return matches


def time_spent_search(time_spent):
    """Search database by time spent"""
    entries = Entry.select().where(Entry.time_spent == time_spent).order_by(
        Entry.date.desc()
    )
    matches = []
    for entry in entries:
        matches.append({
                'employee_name': entry.employee_name,
                'date': entry.date,
                'task_name': entry.task_name,
                'time_spent': entry.time_spent,
                'optional_notes': entry.optional_notes
            })
    return matches


def exact_search(exact_string):
    """Search database task_name and optional_notes fields by exact string"""
    entries = Entry.select().where(
        Entry.task_name.contains(
            exact_string) | Entry.optional_notes.contains(exact_string)
            ).order_by(Entry.date.desc())
    matches = []
    for entry in entries:
        matches.append({
                'employee_name': entry.employee_name,
                'date': entry.date,
                'task_name': entry.task_name,
                'time_spent': entry.time_spent,
                'optional_notes': entry.optional_notes
            })
    return matches


def employee_name_search(employee_name):
    """Searches database by employee name"""
    entries = Entry.select().where(
        Entry.employee_name.contains(employee_name)
    ).order_by(Entry.date.desc())
    matches = []
    for entry in entries:
        matches.append({
                'employee_name': entry.employee_name,
                'date': entry.date,
                'task_name': entry.task_name,
                'time_spent': entry.time_spent,
                'optional_notes': entry.optional_notes
            })
    return matches
