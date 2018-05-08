#!/usr/bin/env python3
"""
This module parses a formatted file of activities throughout the day and
classifies each time partition as Worthy, Neither or Rest.
"""
import os.path
import re
import sqlite3
from datetime import datetime, timedelta

from classify import Classifier

class Parser:
    """
    A file parser that returns a dictionary with information.
    """
    def __init__(self):
        pass

    def parse_file(self, filename):
        """
        Parses the file with given filename and returns a dictionary with info
        of classification of actions in the file.
        """
        lines = self.preprocess_file(filename)
        parsed_list = self.parse_lines(lines)

        return parsed_list

    @staticmethod
    def preprocess_file(filename):
        """
        Preprocesses specified file and returns list of lines.
        """
        with open(filename, encoding='utf-8') as input_file:
            lines = input_file.readlines()
            lines = [line.strip() for line in lines]
            lines = [line for line in lines if line[0] != '#']

        return lines

    def parse_lines(self, lines):
        """
        Parses the given list of lines and returns a dictionary with info
        of classification of actions in the lines.
        """
        parsed_list = []
        last_timestamp = timedelta(hours=0, minutes=0)
        is_pm = False
        for line in lines:
            if line == '~':
                is_pm = True
                continue

            timestamp, actions = self.parse_line(line, is_pm)
            parsed_list.append({
                'start_time': last_timestamp,
                'end_time': timestamp,
                'duration': timestamp - last_timestamp,
                'actions': actions
            })
            last_timestamp = timestamp

        return parsed_list

    def parse_line(self, line, is_pm):
        """
        Parses the given line and returns a dictionary with classification
        of the line.
        """
        timestamp, actions = line[0:5], line[5:].split('/')
        timestamp = self.string_to_timedelta(timestamp.strip(), is_pm)
        actions = [action.strip() for action in actions]

        return (timestamp, actions)

    def string_to_timedelta(self, string, is_pm):
        """
        Converts string-type timestamp to timedelta-type timestamp.

        Examples
        --------
        string_to_timedelta('000') == timedelta(hours=0, minutes=0)
        string_to_timedelta('030') == timedelta(hours=0, minutes=30)
        string_to_timedelta('100') == timedelta(hours=1, minutes=0)
        string_to_timedelta('1200') == timedelta(hours=12, minutes=0)
        """
        if len(string) == 3:
            hours = int(string[0])
            minutes = int(string[1:3])
        elif len(string) == 4:
            hours = int(string[0:2])
            minutes = int(string[2:4])

        if is_pm:
            hours += 12

        return timedelta(hours=hours, minutes=minutes)

if __name__ == '__main__':
    parser = Parser()
    parsed_list = parser.parse_file('LOG-2018-05-02.txt')
    print(parsed_list)


def _timedelta_to_minutes(time):
    """
    Translates given timedelta to minutes and returns it
    """
    return time.seconds // 60

def _timedelta_to_string(time):
    """
    Returns HH:MM format string from given timedelta
    """
    return str(time.seconds // 3600).zfill(2) + ':' + \
        str((time.seconds // 60) % 60).zfill(2)

def _log_unclassified(line):
    """
    Appends given line to a log for later review
    """
    with open('unclassified.log', 'a+') as log:
        log.write(line + '\n')


def _save_to_db(date_str, worthy_str, neither_str, rest_str):
    """
    Save given date_str, worthy_str, neither_str, and rest_str to a SQLite 3
    database.
    """
    if not os.path.exists('db.sqlite3'):
        # Create DB
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute((
            'CREATE TABLE record (date_str text, worthy text'
            ', neither text, rest text)'))
        print('Created new database.')
    else:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

    # Insert Data
    cursor.execute('INSERT INTO record VALUES (?, ?, ?, ?)'
                   , [date_str, worthy_str, neither_str, rest_str])

    conn.commit()
    conn.close()

    print('Saved to database.')

def _update_dict(dictionary, key, time):
    """
    Given dictionary of action (string) keys and duration (int) values,
    creates new key value pair in if key does not exist, otherwise increments
    value of given key.
    """
    if key in dictionary:
        dictionary[key] += _timedelta_to_minutes(time)
    else:
        dictionary[key] = _timedelta_to_minutes(time)

def _is_date_string(string):
    """
    Return True if the given string is formatted YYYY-MM-DD. Returns false if
    not.
    """
    # Check length
    if len(string) != 10:
        return False

    try:
        datetime.strptime(string, "%Y-%m-%d")
    except ValueError:
        return False

    return True

def _get_date_from_filename(filename):
    """
    If filename has the format YYYY-MM-DD.*, return the date string. If not,
    return None.
    """
    # Ignore extension name
    if '.' in filename:
        date_str = filename.split('.', 1)[0]

    # Check format
    if _is_date_string(date_str):
        return date_str

    return None

def parse_file(filename):
    """
    Parse a file with given filename to classify activities.
    """
    # Get Data
    with open(filename, encoding='utf-8') as input_file:
        lines = input_file.readlines()
        lines = [line.strip() for line in lines]
        lines = [line for line in lines if line[0] != '#']

    # Get Date
    date_str = _get_date_from_filename(filename)
    if date_str is None:
        while True:
            date_str = input('What is the date (YYYY-MM-DD)? ')
            if _is_date_string(date_str):
                break
            else:
                print('Wrong format. Please use (YYYY-MM-DD) format.')

    # Total time
    previous_time = timedelta(0)
    worthy_time = timedelta(0)
    neither_time = timedelta(0)
    rest_time = timedelta(0)

    # Dictionary of Actions
    worthy_dict = {}
    neither_dict = {}
    rest_dict = {}

    # Parse File
    # TODO Use Parser

    # Classify actions
    # TODO Use Classifier

    worthy_str = _timedelta_to_string(worthy_time)
    neither_str = _timedelta_to_string(neither_time)
    rest_str = _timedelta_to_string(rest_time)

    print('Worthy  : ' + worthy_str)
    print('Neither : ' + neither_str)
    print('Rest    : ' + rest_str)

    # Save to SQLite3 Database
    _save_to_db(date_str, worthy_str, neither_str, rest_str)

    # Format data
    summary = [
        {'label': 'Worthy', 'duration': _timedelta_to_minutes(worthy_time)},
        {'label': 'Neither', 'duration': _timedelta_to_minutes(neither_time)},
        {'label': 'Rest', 'duration': _timedelta_to_minutes(rest_time)}
    ]

    # Get sorted lists from dictionaries
    worthy_list = [{'label': k, 'duration': worthy_dict[k]} for k \
        in sorted(worthy_dict, key=worthy_dict.get, reverse=True)]
    neither_list = [{'label': k, 'duration': neither_dict[k]} for k \
        in sorted(neither_dict, key=neither_dict.get, reverse=True)]
    rest_list = [{'label': k, 'duration': rest_dict[k]} for k \
        in sorted(rest_dict, key=rest_dict.get, reverse=True)]

    return {
        'date': date_str,
        'summary': summary,
        'worthy_list': worthy_list,
        'neither_list': neither_list,
        'rest_list': rest_list
    }
