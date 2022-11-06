# work-log-with-database
* This CLI lets employees enter work log entries consisting of their name, date, task title, time spent, and optional
notes into a database
* Entries in the database can be viewed, edited, or deleted and records can be found by searching on employee, exact date, range of dates, time spent, or by term (string) to find any entries containing that string in either the task name or in the optional notes 

## See
* [test.py](https://github.com/FVPukay/work-log-with-a-database/blob/master/test.py)
    * Unit tests and coverage.py
    * Test coverage is 99%
* [work_log.py](https://github.com/FVPukay/work-log-with-a-database/blob/master/work_log.py) to see the controller
* [work_log_db.py](https://github.com/FVPukay/work-log-with-a-database/blob/master/work_log_db.py) to see the database models
    * [Peewee ORM](http://docs.peewee-orm.com/en/latest/) is utilized

## Screenshots
* See [these photos](https://www.flickr.com/photos/156561177@N03/albums/72157679623961018)

## How to run
* There are 3 Python files and a requirements file: [work_log.py](https://github.com/FVPukay/work-log-with-a-database/blob/master/work_log.py), [work_log_db.py](https://github.com/FVPukay/work-log-with-a-database/blob/master/work_log_db.py),
[test.py](https://github.com/FVPukay/work-log-with-a-database/blob/master/test.py), and [requirements.txt](https://github.com/FVPukay/work-log-with-a-database/blob/master/requirements.txt)
* The code is written using Python 3 so the following command can be entered in the terminal to run the application

>`python3 work_log.py`
