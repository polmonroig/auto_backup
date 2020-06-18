#!/usr/bin/python3
import paths
import os


gigabyte = 1000000000
megabyte = 1000000
kilobyte = 1000

def add_project(projects, root, sep, project, client):
    name = os.path.join(client, project)
    if name in projects:
        if root in projects[name]:
            projects[name][root].append(sep)
        else:
            projects[name][root] = [sep]
    else:
        projects[name] = {}
        projects[name][root] = [sep]

    return projects

# WORK/PROJECT/client/projectName
def find_clients(projects, root, sep):
    path = os.path.join(root, sep)
    if os.path.exists(path):
        for client in os.listdir(path): # client
            client_path = os.path.join(path, client)
            if os.path.isdir(client_path):
                for project in os.listdir(client_path):
                    project_path = os.path.join(client_path, project)
                    if os.path.isdir(project_path):
                        projects = add_project(projects, root, sep, project, client)
    return projects

def get_projects():
    projects = {}
    for root in paths.root_dirs: # work, storage, backup
        for sep in paths.separation_dirs: # project, footage, cache, render
            projects = find_clients(projects, root, sep)
    return projects



def recursive_get_size(path):
    if os.path.isdir(path):
        return sum([recursive_get_size(os.path.join(path, file)) for file in os.listdir(path)])
    else:
        return os.path.getsize(path)


def format_size(size):
    size /= gigabyte
    size = "{:.3f}".format(size) + ' GB'
    return size

def get_size(p, separations, root, name, separation):
    dir_size = 'NA'
    for sep in separations:
        if sep == separation:
            path = os.path.join(root, sep, p)
            size = recursive_get_size(path)
            dir_size = format_size(size)
            break

    return dir_size

def print_separation(p, projects, name, sep):
    print(sep)
    sep = sep + '/'
    work_size = 'NA'
    storage_size = 'NA'
    backup_size = 'NA'
    if paths.work_dir in projects[name]:
        work = projects[name][paths.work_dir]
        work_size = get_size(p, work, paths.work_dir, paths.work_name, sep)
    if paths.storage_dir in projects[name]:
        storage = projects[name][paths.storage_dir]
        storage_size = get_size(p, storage, paths.storage_dir, paths.storage_name, sep)
    if paths.backup_dir in projects[name]:
        backup = projects[name][paths.backup_dir]
        backup_size = get_size(p, backup, paths.backup_dir, paths.backup_name, sep)

    print('     '+ paths.work_name +'........ ' + work_size)
    print('     '+ paths.storage_name +' .... ' + storage_size)
    print('     '+ paths.backup_name +' ........ ' + backup_size)

def print_project(projects, p):
    p_split = p.split('/')
    client, project = p_split[0], p_split[1]
    name = os.path.join(client, project)
    if not (name in projects):
        print('No project satisfies the requested name.')
        print('The project must be identified by client/project')
    else:
        print(name)
        print_separation(p, projects, name, paths.project_name)
        print_separation(p, projects, name, paths.footage_name)
        print_separation(p, projects, name, paths.render_name)
        print_separation(p, projects, name, paths.cache_name)






def print_all(projects):
    ids = projects.keys()
    for id in ids:
        print_project(projects, id)
        print("========================================")

def print_client(projects, client):
    keys = projects.keys()
    selected_projects = []
    for key in keys:
        arr = key.split('/')
        if arr[0] == client:
            selected_projects.append(key)
    for id in selected_projects:
        print_project(projects, id)
        print("========================================")

def usage():
    print('Welcome to the automatic project backup manager!\n')
    print('This application has some basic commands')
    print('    help: is how you got here')
    print('    fetch [project/client/all]: displays information about a set of files')
    print('    copy [project] [category] [from] [to]: copies files from a project into the corresponding directory\n')

def ask_info(projects):
    # print(projects)
    print('Type "help", "fetch", "copy".')
    command = input('>> ')
    while command != 'exit':
        command = command.split()
        if command[0] == 'help':
            usage()
        elif command[0] == 'fetch' and len(command) >= 2:
            if command[1] == 'all':
                print_all()
            elif command[1] == 'client' and len(command) >= 3:
                print_client(projects, command[2])
            elif command[1] == 'project' and len(command) >= 3:
                print_project(projects, command[2]) 

        elif command[0] == 'copy':
            print('Sorry, currently not implemented')

        command = input('>>> ')




def main():
    print('Initializing...')
    projects = get_projects()
    if projects != None:
        ask_info(projects)
    else:
        print('No files where found, exiting application...')




if __name__ == '__main__':
    main()
