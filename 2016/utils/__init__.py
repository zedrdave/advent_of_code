import os
import tty
import termios
import sys
import pytz
import datetime
import time
import webbrowser
from collections import defaultdict
import numpy as np
import requests
import inspect


def cmp(a, b): return (a > b) - (a < b)


def dl_input(day, sc='session_cookie.txt', year=None):
    """sc - path to file containing session cookie value, or value as string"""
    if year is None:
        year = datetime.datetime.now().year

    try:
        day = int(day)
    except:
        raise ValueError("day must be a number")

    if day < 1 or day > 25:
        raise ValueError("day must be in the range 1 <= day <= 25")

    if sc is not None:
        try:
            with open(sc) as fh:
                sc = fh.read().strip()
        except:
            sc = sc.strip()
    else:
        raise ValueError("session cookie must be provided")

    url = f"https://adventofcode.com/{year}/day/{day}/input"

    r = requests.get(url, cookies={'session': sc})

    if r.status_code == 200:
        txt = r.text.strip()
        if not os.path.exists(f'{day:02}'):
            os.mkdir(f'{day:02}')
        with open(f'{day:02}/input.txt', 'w') as f:
            f.write(txt)
        return txt
    elif r.status_code == 404:
        print(f"{url} returned:", r.text)
        return False
    else:
        raise IOError("Server responded {}: {}\n"
                      "This probably means you have a bad/expired "
                      "session cookie".format(r.status_code, r.reason))


def countdown(year=None):
    if year is None:
        year = datetime.datetime.now().year

    dt = datetime.datetime.now(pytz.timezone('EST'))

    if dt.hour < 23:
        print(
            f"Current EST time is {dt.strftime('%H:%M (%d/%m)')}. Try again in ~{23-dt.hour} hours…")
        return None

    wait_sec = (59-dt.minute) * 60 + (59-dt.second)

    new_day = dt.day % 30 + 1
    print(
        f"Current EST time is {dt.strftime('%H:%M:%S (%d/%m)')}. Will try to get day {new_day} in {wait_sec//60}m{wait_sec%60}s.")

    if wait_sec > 10:
        time.sleep(wait_sec-10)

    remaining = min(10, wait_sec)
    for n in range(0, remaining):
        print(f"{remaining-n}…", end=' ')
        time.sleep(1)

    print("It's time!")
    while True:
        pb_input = dl_input(new_day, year=year)
        if pb_input is not False:
            break
        print('.', end='')
        time.sleep(.2)

    print("************ GO! *************")
    print(datetime.datetime.now(pytz.timezone('EST')))

    webbrowser.open(f'https://adventofcode.com/{year}/day/{new_day}', new=2)

    return pb_input


def input_file(day=None, year=None, file='input.txt'):
    if year is None:
        year = datetime.datetime.now().year

    if day is None:
        for frm in inspect.stack():
            mod = inspect.getmodule(frm[0])
            if mod is None:
                raise Exception(
                    "Need to provide day if not calling as package")
            if not mod.__file__.endswith('utils/__init__.py'):
                break
        if mod.__file__.endswith('utils/__init__.py'):
            raise Exception("Need to provide day if not calling from subdir")
        return os.path.join(os.path.dirname(mod.__file__), file)
    else:
        return os.path.join(os.getcwd(), f'{day:02}', file)


def load_string_input(day=None, file='input.txt'):
    with open(input_file(day, file)) as f:
        return [s.strip() for s in f.readlines()]


def load_int_input(day=None, file='input.txt'):
    with open(input_file(day, file)) as f:
        return [int(i.strip()) for i in f.readlines()]


def load_CSV_input(day=None, file='input.txt'):
    with open(input_file(day, file)) as f:
        return [int(i.strip()) for i in f.read().split(',')]


def load_XYZ_input(day=None):
    with open(input_file(day)) as f:
        return [[int(pos[2:]) for pos in l.strip()[1:-1].split(', ')] for l in f]


def set_verbosity(level):
    os.environ['VERBOSE'] = str(int(level))


def is_verbose():
    return int(os.environ.get('VERBOSE', 0)) > 0


def dprint(*pargs, **kwargs):
    if isVerbose():
        print(*pargs, **kwargs)


def sparse_to_dense(bitmap):
    # import scipy.sparse

    items = list(bitmap.items())
    vs = [v for (i, j), v in items]
    ii = [i for (i, j), v in items]
    min_ii = min(ii)
    ii = [i-min_ii for i in ii]  # avoid negative indices
    jj = [j for (i, j), v in items]
    min_jj = min(jj)
    jj = [i-min_jj for i in jj]  # avoid negative indices
    # Todo: load better
    arr = np.zeros((max(ii)+1, max(jj)+1), 'int8')
    for i, j, v in zip(ii, jj, vs):
        arr[i][j] = v
    return arr
    # return scipy.sparse.csr_matrix((vs, (ii, jj))).toarray()


def get_char():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
