from parser import Parser
import paths
import os

class ProjectDatabase:

    GIGABYTE = 1000000000
    MEGABYTE = 1000000
    KILOBYTE = 1000

    def __init__(self):
        self.projects = {}
        self.actions = {Parser.INCORRECT_COMMAND : None,
                        Parser.PRINT_ALL : self.print_all,
                        Parser.PRINT_CLIENT : self.print_client,
                        Parser.PRINT_PROJECT : self.print_project,
                        Parser.LIST_PROJECTS : self.list_projects,
                        Parser.LIST_CLIENTS : self.list_clients,
                        Parser.LIST_PROJECTS_IN : self.list_projects_in}

    def empty(self):
        return len(self.projects) == 0

    def load(self):
        for root in paths.root_dirs: # work, storage, backup
            for sep in paths.separation_dirs: # project, footage, cache, render
                self.find_clients(root, sep)

    def interact(self, action):
        if action[0] != Parser.IGNORE_COMMAND:
            if action[1] == None:
                self.actions[action[0]]()
            else:
                self.actions[action[0]](action[1])

    def add_project(self, root, sep, project, client):
        name = os.path.join(client, project)
        if name in self.projects:
            if root in self.projects[name]:
                self.projects[name][root].append(sep)
            else:
                self.projects[name][root] = [sep]
        else:
            self.projects[name] = {}
            self.projects[name][root] = [sep]


    # WORK/PROJECT/client/projectName
    def find_clients(self, root, sep):
        path = os.path.join(root, sep)
        if os.path.exists(path):
            for client in os.listdir(path): # client
                client_path = os.path.join(path, client)
                if os.path.isdir(client_path):
                    for project in os.listdir(client_path):
                        project_path = os.path.join(client_path, project)
                        if os.path.isdir(project_path):
                            self.add_project(root, sep, project, client)


    def print_separation(self, p, name, sep):
        print(sep)
        work_size = 'NA'
        storage_size = 'NA'
        backup_size = 'NA'
        if paths.work_dir in self.projects[name]:
            work = self.projects[name][paths.work_dir]
            work_size = ProjectDatabase.get_size(p, work, paths.work_dir, paths.work_name, sep)
        if paths.storage_dir in self.projects[name]:
            storage = self.projects[name][paths.storage_dir]
            storage_size = ProjectDatabase.get_size(p, storage, paths.storage_dir, paths.storage_name, sep)
        if paths.backup_dir in self.projects[name]:
            backup = self.projects[name][paths.backup_dir]
            backup_size = ProjectDatabase.get_size(p, backup, paths.backup_dir, paths.backup_name, sep)

        print('     '+ paths.work_name +'........ ' + work_size)
        print('     '+ paths.storage_name +' .... ' + storage_size)
        print('     '+ paths.backup_name +' ........ ' + backup_size)

    def print_project(self, p):
        p_split = p.split('/')
        client, project = p_split[0], p_split[1]
        name = os.path.join(client, project)
        if not (name in self.projects):
            print('No project satisfies the requested name.')
            print('The project must be identified by client/project')
        else:
            print(name)
            for sep in paths.separation_names:
                self.print_separation(p, name, sep)

    def print_all(self):
        ids = self.projects.keys()
        for id in ids:
            self.print_project(id)
            print("========================================")

    def print_client(self, client):
        keys = self.projects.keys()
        selected_self.projects = []
        for key in keys:
            arr = key.split('/')
            if arr[0] == client:
                selected_self.projects.append(key)
        for id in selected_self.projects:
            self.print_project(id)
            print("========================================")



    def list_projects(self):
        keys = self.projects.keys()
        for key in keys:
            print(key)

    def list_clients(self):
        keys = self.projects.keys()
        clients = set()
        for key in keys:
            key = key.split('/')
            clients.add(key[0])
        for client in clients:
            print(client)

    def list_projects_in(self, client):
        keys = self.projects.keys()
        for key in keys:
            key = key.split('/')
            if key[0] == client:
                print(key[1])


    # STATIC
    @staticmethod
    def recursive_get_size(path):
        if os.path.isdir(path):
            return sum([ProjectDatabase.recursive_get_size(os.path.join(path, file)) for file in os.listdir(path)])
        else:
            return os.path.getsize(path)

    @staticmethod
    def format_size(size):
        size /= ProjectDatabase.GIGABYTE
        size = "{:.3f}".format(size) + ' GB'
        return size

    @staticmethod
    def get_size(p, separations, root, name, separation):
        dir_size = 'NA'
        for sep in separations:
            tmp = sep.split('/')[-2]
            if tmp == separation:
                path = os.path.join(root, sep, p)
                size = ProjectDatabase.recursive_get_size(path)
                dir_size = ProjectDatabase.format_size(size)
                break

        return dir_size
