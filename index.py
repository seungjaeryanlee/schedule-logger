import os.path
import re
import sqlite3
from datetime import timedelta

# Get Regex
with open('worthy.regex') as file:
    wRegex = file.readlines()
    wRegex = [regex.strip() for regex in wRegex]
with open('rest.regex') as file:
    rRegex = file.readlines()
    rRegex = [regex.strip() for regex in rRegex]
with open('neither.regex') as file:
    nRegex = file.readlines()
    nRegex = [regex.strip() for regex in nRegex]

def timeDeltaToString(td):
    return str(td.seconds//3600).zfill(2) + ':' + str((td.seconds//60)%60).zfill(2);

def parseActions(actions):
    for regex in wRegex:
        for action in actions:
            if re.search(regex, action):
                return 'W'

    for regex in nRegex:
        for action in actions:
            if re.search(regex, action):
                return 'N'

    for regex in rRegex:
        for action in actions:
            if re.search(regex, action):
                return 'R'

    return 'X';

def saveToDB(worthyString, restString):
    if not os.path.exists('db.sqlite3'):
        # Create DB
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE day (worthy text, rest text)')
        print('Created new database.')
    else:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

    # Insert Data
    cursor.execute('INSERT INTO day VALUES (?, ?)', [worthyString, restString])
    
    conn.commit()
    conn.close()

    print('Saved to database.')

def parseFile(filename):
    # Get Data
    with open(filename, encoding='utf-8') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        lines = [line for line in lines if line[0] != '#']

    # Parse
    previousTime = timedelta(0)
    worthyTime = timedelta(0)
    restTime = timedelta(0)
    for line in lines:
        tokens = line.split('/')
        tokens = [token.strip() for token in tokens]

        # Parse Time and Calculte Delta
        hour, minute = tokens[0].split(':')
        thisTime = timedelta(hours=int(hour), minutes=int(minute))
        deltaTime = thisTime - previousTime
        previousTime = thisTime
        tokens.pop(0)

        # Parse tokens
        result = parseActions(tokens)
        if result == 'W':
            worthyTime += deltaTime
        elif result == 'R':
            restTime += deltaTime
        elif result == 'N':
            pass
        else:
            # Ask user
            while True:
                print(line)
                answer = input('Should the event above be marked W, R or N? (W, R, N): ')
                if answer == 'W':
                    worthyTime += deltaTime;
                    break
                elif answer == 'R':
                    restTime += deltaTime;
                    break
                elif answer == 'N':
                    break
                else:
                    print('Unrecognized output: type W for worthy, R for rest, or N for neither')

    worthyString = timeDeltaToString(worthyTime)
    restString = timeDeltaToString(restTime)

    print('Worthy : ' + worthyString)
    print('Rest   : ' + restString)

    # Save to SQLite3 Database
    saveToDB(worthyString, restString)

parseFile('log.txt')