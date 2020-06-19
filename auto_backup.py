#!/usr/bin/python3
from version import __version__
from parser import Parser
from database import ProjectDatabase


def init(database):
    parser = Parser()
    for action in parser.loop():
        database.interact(action)


def main():
    print('Backup utility', __version__)
    database = ProjectDatabase()
    init(database)


if __name__ == '__main__':
    main()
