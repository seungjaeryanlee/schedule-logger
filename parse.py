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
        last_timestamp = '000' # TODO: Use actual "time"
        for line in lines:
            timestamp, actions = self.parse_line(line)
            parsed_list.append({ 'start_time': last_timestamp, 'end_time': timestamp, 'actions': actions })
            last_timestamp = timestamp

        return parsed_list

    def parse_line(self, line):
        """
        Parses the given line and returns a dictionary with classification
        of the line.
        """
        timestamp, actions = line[0:5], line[5:].split('/')
        timestamp = timestamp.strip()
        actions = [action.strip() for action in actions]

        return (timestamp, actions)

if __name__ == '__main__':
    parser = Parser()
    parsed_list = parser.parse_file('LOG-2018-05-02.txt')
    print(parsed_list)



TIMESTAMP_NO_COLON = True

# Get Regex
with open('worthy.regex') as file:
    WORTHY_REGEX = file.readlines()
    WORTHY_REGEX = [regex.strip() for regex in WORTHY_REGEX]
with open('neither.regex') as file:
    NEITHER_REGEX = file.readlines()
    NEITHER_REGEX = [regex.strip() for regex in NEITHER_REGEX]
with open('rest.regex') as file:
    REST_REGEX = file.readlines()
    REST_REGEX = [regex.strip() for regex in REST_REGEX]

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

def _get_timedelta_from_string(string):
    """
    Return timedelta from HHMM formatted string if TIMESTAMP_NO_COLON = True,
    or HH:MM formatted string if TIMESTAMP_NO_COLON = False
    """

    if TIMESTAMP_NO_COLON:
        if len(string) == 3:
            hour = string[0]
            minute = string[1:3]
        else: # len(string) == 4
            hour = string[0:2]
            minute = string[2:4]
    else:
        hour, minute = string.split(':')

    return timedelta(hours=int(hour), minutes=int(minute))

def _log_unclassified(line):
    """
    Appends given line to a log for later review
    """
    with open('unclassified.log', 'a+') as log:
        log.write(line + '\n')

def _parse_actions(line, actions):
    """
    Return 'W' (Worthy), 'N' (Neither), 'R' (Rest), 'X' (Unclassified) after
    classifying given actions with regex. If 'X' (Unclassified), the line is
    logged for review.

    The classification algorithm follows:
    1. If there is a worthy action, the line is classified worthy.
    2. If there is no worthy action, and there is an unclassified action, the
       line is unclassified.
    3. If there is no worthy action or unclassified action, if there is a
       neither action, the line is classified neither.
    4. If there is no worthy or unclassified or neither action, the line is
       classified rest.
    """

    has_worthy = False
    has_neither = False
    has_rest = False
    has_unclassified = False

    # Check all actions and see which type of actions the line has
    for action in actions:
        is_classified = False
        for regex in WORTHY_REGEX:
            if re.search(regex, action):
                is_classified = True
                has_worthy = True
        for regex in NEITHER_REGEX:
            if re.search(regex, action):
                is_classified = True
                has_neither = True
        for regex in REST_REGEX:
            if re.search(regex, action):
                is_classified = True
                has_rest = True
        if not is_classified:
            has_unclassified = True

    # Classify line based on the actions
    if has_worthy:
        return 'W'
    if has_unclassified:
        _log_unclassified(line)
        return 'X'
    if has_neither:
        return 'N'
    if has_rest:
        return 'R'

    # Should never reach since every action is classified as one of the four
    return 'X'


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

    # Whether the time is after 12:59 and should be converted to 24-hour format
    is_pm = False


    for line in lines:
        # Check if the line is a PM token ('~')
        if line[0] == '~':
            is_pm = True
            continue

        # Parse time
        time_str = line[0:5].strip()
        this_time = _get_timedelta_from_string(time_str)

        # If after 12:59, add 12 hours to make it 24-hour format
        if is_pm:
            this_time += timedelta(hours=12)

        # Calculate timedelta
        delta_time = this_time - previous_time
        previous_time = this_time

        # Parse actions
        tokens = line[5:].split('/')
        tokens = [token.strip() for token in tokens]

        # Classify actions
        result = _parse_actions(line, tokens)
        if result == 'W':
            worthy_time += delta_time
            _update_dict(worthy_dict, line[5:], delta_time)
        elif result == 'N':
            neither_time += delta_time
            _update_dict(neither_dict, line[5:], delta_time)
        elif result == 'R':
            rest_time += delta_time
            _update_dict(rest_dict, line[5:], delta_time)
        else:
            # Ask user
            while True:
                print(line)
                answer = input(
                    'Should the event above be marked W, N or R? (W, N, R): ')
                if answer == 'W':
                    worthy_time += delta_time
                    _update_dict(worthy_dict, line[5:], delta_time)
                    break
                elif answer == 'N':
                    neither_time += delta_time
                    _update_dict(neither_dict, line[5:], delta_time)
                    break
                elif answer == 'R':
                    rest_time += delta_time
                    _update_dict(rest_dict, line[5:], delta_time)
                    break
                else:
                    print((
                        'Unrecognized output: type W for worthy, N for neither'
                        ', or R for rest,'
                    ))

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
