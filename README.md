# work-log-with-database

##### What this application does
This terminal application lets employees enter work log entries
consisting of their name, date, task title, time spent, and optional
notes into a database (Sqlite).  Entries in the database can be viewed,
edited, or deleted and records can be found by searching on employee,
exact date, range of dates, time spent, or by term (string) to find any
entries containing that string in either the task name or in the optional
notes.  

Unit tests and coverage.py are utilized.  Test coverage is 99%.

##### Screenshots of the UI
Here are images of the work_log.py UI   
[work_log_with_database UI](https://www.flickr.com/photos/156561177@N03/albums/72157679623961018)

##### How to run work_log.py
There are 3 Python files and a requirements file: work_log.py, work_log_db.py,
test.py, and requirements.txt.  The code is written using Python 3 so the
following command can be entered in the terminal to run the application.

>`python3 work_log.py`
