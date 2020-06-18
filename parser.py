import readline


class Parser:

    INCORRECT_COMMAND = 0
    IGNORE_COMMAND = 1
    PRINT_ALL = 2
    PRINT_CLIENT = 3
    PRINT_PROJECT = 4

    LIST_PROJECTS = 5
    LIST_CLIENTS = 6
    LIST_PROJECTS_IN = 7



    def __init__(self):
        self.commands = [('help', 'is how you got here'),
                         ('fetch ', '[project/client/all] [name]: displays information about a set of files'),
                         ('copy', '[project] [category] [from] [to]: copies files from a project into the corresponding directory'),
                         ('list', '[clients/projects] (in client)?: displays a list of the possible clients and projects'),
                         ('exit', ':exits application')]
        self.command = None

    def usage(self):
        print('Welcome to the automatic project backup utility!\n')
        for command in self.commands:
            print('   ', command[0], command[1])
        print()

    def read(self):
        self.command = input('>>> ').split()

    def parse(self):
        if self.command[0] == 'help':
            self.usage()
            return (Parser.IGNORE_COMMAND, None)
        elif self.command[0] == 'fetch' and len(self.command) >= 2:
            if self.command[1] == 'all':
                return (Parser.PRINT_ALL, None)
            elif self.command[1] == 'client' and len(self.command) >= 3:
                return (Parser.PRINT_CLIENT, self.command[2])
            elif self.command[1] == 'project' and len(self.command) >= 3:
                return (Parser.PRINT_PROJECT, self.command[2])
        elif self.command[0] == 'list' and len(self.command) >= 2:
            if self.command[1] == 'projects':
                if len(self.command) >= 4 and self.command[2] == 'in':
                    return (Parser.LIST_PROJECTS_IN, self.command[3])
                else:
                    return (Parser.LIST_PROJECTS, None)
            elif self.command[1] == 'clients':
                return (Parser.LIST_CLIENTS, None)
        elif self.command[0] == 'copy':
            return (Parser.INCORRECT_COMMAND, None)

    def loop(self):
        print('Type "help", "fetch", "copy", exit and list.')
        self.read()
        while self.command[0] != 'exit':
            yield self.parse()
            self.read()
