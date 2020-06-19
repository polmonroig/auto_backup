from parser import Parser
from shutil import copyfile
import os
import subprocess

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
                        Parser.LIST_PROJECTS_IN : self.list_projects_in,
                        Parser.COPY_PROJECT : self.copy_project,
                        Parser.LOAD: self.load,
                        Parser.ADD_DATABASE : self.add_database,
                        Parser.ADD_CATEGORY : self.add_category,
                        Parser.EXPLORE : self.explore}
        self.databases = []
        self.categories = []



    def add_database(self, name, dir):
        self.databases.append((name, dir))

    def add_category(self, name, dir):
        self.categories.append((name, dir))

    def empty(self):
        return len(self.projects) == 0

    def load(self):
        self.project = {}
        for root in self.databases: # work, storage, backup
            for sep in self.categories: # project, footage, cache, render
                self.find_clients(root[1], sep[1])
        if self.empty():
            print('No projects were found')

    def interact(self, action):
        if action[0] != Parser.IGNORE_COMMAND:
            if action[1][0] == None:
                self.actions[action[0]]()
            else:
                self.actions[action[0]](*action[1])

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
        for root_name, root_dir in self.databases:
            size = 'NA'
            if root_dir in self.projects[name]:
                root = self.projects[name][root_dir]
                size = ProjectDatabase.get_size(p, root, root_dir, root_name, sep)
            print('     '+ ProjectDatabase.format_dots(root_name, 12) + size)


    def print_project(self, p):
        p_split = p.split('/')
        client, project = p_split[0], p_split[1]
        name = os.path.join(client, project)
        if not (name in self.projects):
            print('No project satisfies the requested name.')
            print('The project must be identified by client/project')
        else:
            print(name)
            for sep in self.categories:
                self.print_separation(p, name, sep[0])

    def print_all(self):
        ids = self.projects.keys()
        for id in ids:
            self.print_project(id)
            print("========================================")

    def print_client(self, client):
        keys = self.projects.keys()
        selected_projects = []
        for key in keys:
            arr = key.split('/')
            if arr[0] == client:
                selected_projects.append(key)
        for id in selected_projects:
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

    def copy_project(self, project, sep, src, dst):
        sep = ProjectDatabase.find_pair(sep, self.categories)
        src = ProjectDatabase.find_pair(src, self.databases)
        dst = ProjectDatabase.find_pair(dst, self.databases)
        src_path = os.path.join(src, sep, project)
        dst_path = os.path.join(dst, sep, project)
        print('Coping from', src_path, 'to', dst_path)
        ProjectDatabase.copy_files(src_path, dst_path)


    def explore(self, project, category, db):
        db = ProjectDatabase.find_pair(db, self.databases)
        category = ProjectDatabase.find_pair(category, self.categories)
        path = os.path.join(db, category, project)
        subprocess.Popen(['nautilus'])

    # STATIC

    @staticmethod
    def copy_files(src, dst):
        if not os.path.exists(dst):
            os.makedirs(dst)
        files = os.listdir(src)
        for file in files:
            complete_src_path = os.path.join(src, file)
            complete_dst_path = os.path.join(dst, file)
            if os.path.isdir(complete_src_path):
                if not os.path.exists(complete_dst_path):
                    os.makedirs(complete_dst_path)
                for sub_file in os.listdir(complete_src_path):
                    files.append(os.path.join(file, sub_file))
            elif not os.path.exists(complete_dst_path):
                copyfile(complete_src_path, complete_dst_path)



    @staticmethod
    def find_pair(fst, array):
        for pair in array:
            if fst == pair[0]:
                return pair[1]
        return None

    @staticmethod
    def format_dots(name, dots):
        name += ' '
        while len(name) < dots:
            name += '.'
        name += ' '
        return name

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
