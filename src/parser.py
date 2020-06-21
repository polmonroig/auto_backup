import readline


class Parser:

    """
    The database parser works by reading the commands of the
    user, interpreting them and yielding a corresponding response.
    The response of the parser is a tuple where the first element
    is the type of responde and the second element is additional
    information that might be needed to handle the interaction.

    The parser is in fact a generator of user inputs, it stops
    yielding inputs when the user stops.
    """

    INCORRECT_COMMAND = 0
    IGNORE_COMMAND = 1
    PRINT_ALL = 2
    PRINT_CLIENT = 3
    PRINT_PROJECT = 4

    LIST_PROJECTS = 5
    LIST_CLIENTS = 6
    LIST_PROJECTS_IN = 7
    LIST_PROJECTS_IN_IN = 8

    COPY_PROJECT = 9
    LOAD = 10
    ADD_DATABASE = 11
    ADD_CATEGORY = 12

    EXPLORE = 13

    def __init__(self):
        self.commands = [('help', 'is how you got here'),
                         ('fetch ', '[project/client/all] [name]: displays information about a set of files'),
                         ('copy', '[project] [category] [from] [to]: copies files from a project into the corresponding directory'),
                         ('list', '[clients/projects] (in client)?: displays a list of the possible clients and projects'),
                         ('load', ': loads the corresponding databases'),
                         ('add', '[database/category]: adds a database or a category to the program'),
                         ('explore', '[project] [category] [database]: opens the file explorer (e.g. nautilus) in the selected project'),
                         ('exit', ':exits application')]
        self.command = None

    def usage(self):
        print('Welcome to the automatic project backup utility!\n')
        for command in self.commands:
            print('   ', command[0], command[1])
        print()

    def read_file(self, file_name):
        fd = open(file_name, 'r')
        for line in fd:
            self.command = line.split()
            yield self.parse()

    def read(self):
        self.command = input('>>> ').split()

    def parse(self):
        if self.command[0] == 'help':
            self.usage()
            return (Parser.IGNORE_COMMAND, (None,))
        elif self.command[0] == 'fetch' and len(self.command) >= 2:
            if self.command[1] == 'all':
                return (Parser.PRINT_ALL, (None,))
            elif self.command[1] == 'client' and len(self.command) >= 3:
                return (Parser.PRINT_CLIENT, (self.command[2],))
            elif self.command[1] == 'project' and len(self.command) >= 3:
                return (Parser.PRINT_PROJECT, (self.command[2],))
        elif self.command[0] == 'list' and len(self.command) >= 2:
            if self.command[1] == 'projects':
                if len(self.command) >= 4 and self.command[2] == 'in':
                    if len(self.command) >= 6 and self.command[4] == 'in':
                        return (Parser.LIST_PROJECTS_IN_IN, (self.command[3], self.command[5]))
                    else:
                        return (Parser.LIST_PROJECTS_IN, (self.command[3],))
                else:
                    return (Parser.LIST_PROJECTS, (None,))
            elif self.command[1] == 'clients':
                return (Parser.LIST_CLIENTS, (None,))
        elif self.command[0] == 'copy':
            return (Parser.COPY_PROJECT, (self.command[1],
                    self.command[2], self.command[3], self.command[4]))
        elif self.command[0] == 'load':
            return (Parser.LOAD, (None, ))
        elif self.command[0] == 'add' and len(self.command) >= 3:
            if self.command[1] == 'database':
                return (Parser.ADD_DATABASE, (self.command[2], self.command[3]))  # name location
            elif self.command[1] == 'category':
                return (Parser.ADD_CATEGORY, (self.command[2], self.command[3]))
        elif self.command[0] == 'explore':
            return (Parser.EXPLORE, (self.command[1], self.command[2], self.command[3]))

        return (Parser.IGNORE_COMMAND, (None))

    def loop(self):
        print('Type "help", "fetch", "copy", "exit" and "list".')
        self.read()
        while self.command[0] != 'exit':
            yield self.parse()
            self.read()
