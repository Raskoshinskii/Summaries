import json
import os
import sys
from datetime import datetime, timedelta


def doSomething():
    x = 10
    y = 20
    # Bad use of whitespaces and semicolons, and poor variable naming
    print("X+y=", x + y)


def checkDate():
    now = datetime.now()
    then = datetime(2020, 1, 1)
    if now - then > timedelta(days=100):
        print("It's been more than 100 days since the start of 2020")


import random


def main():
    doSomething()
    checkDate()


main()
