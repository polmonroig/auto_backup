import readline


class Parser:

    INCORRECT_COMMAND = 0

    PRINT_ALL = 1
    PRINT_CLIENT = 2
    PRINT_PROJECT = 3

    LIST_PROJECTS = 4
    LIST_CLIENTS = 5
    LIST_PROJECTS_IN = 6

    def __init__(self):
        self.commands = [('help', 'is how you got here'),
                         ('fetch ', '[project/client/all] [name]: displays information about a set of files'),
                         ('copy', '[project] [category] [from] [to]: copies files from a project into the corresponding directory')
                         ('list', '[clients/projects] (in client)?: displays a list of the possible clients and projects'),
                         ('exit', ':exits application')]
        self.command = None

    def usage(self):
        print('Welcome to the automatic project backup utility!\n')
        for command in self.commands:
            print(command[0], command[1])
        print()

    def read(self):
        self.command = input('>>> ').split()

    def parse(self):
        if command[0] == 'help':
            self.usage()
        elif command[0] == 'fetch' and len(command) >= 2:
            if command[1] == 'all':
                return (Parser.PRINT_ALL, None)
            elif command[1] == 'client' and len(command) >= 3:
                return (Parser.PRINT_CLIENT, command[2])
            elif command[1] == 'project' and len(command) >= 3:
                return (Parser.PRINT_PROJECT, command[2])
        elif command[0] == 'list' and len(command) >= 2:
            if command[1] == 'projects':
                if len(command) >= 4 and command[2] == 'in':
                    return (Parser.LIST_PROJECTS_IN, command[3])
                else:
                    return (Parser.LIST_PROJECTS, None)
            elif command[1] == 'clients':
                return (Parser.LIST_CLIENTS, None)
        elif command[0] == 'copy':
            yield (Parser.INCORRECT_COMMAND, None)

    def loop(self):
        print('Type "help", "fetch", "copy", exit and list.')
        self.read()
        while command != 'exit':
            yield self.parse()
            self.read()
