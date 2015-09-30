import os

__author__ = 'oyakov'

data_dir = os.getcwd()

###############################################
#          CLI commands definitions           #
###############################################


def data_dir(new_data_dir, isset):
    global data_dir
    if set:
        data_dir = new_data_dir
    else:
        print(data_dir)


def dir_stat():
    pass


def file_constr():
    pass


def read_files():
    pass


def analyze_buf():
    pass


###############################################
#                 Mappings                    #
###############################################


commands = {
    'ddir': data_dir,
    'dirs': dir_stat,
    'analyze': analyze_buf(),
    'fcons': file_constr,
    'quit': quit
}


###############################################
#             Parser definitions              #
###############################################


def parse_input(comm):
    terms = comm.split(' ')
    return terms.pop(), terms


###############################################
#                 Main flow                   #
###############################################


if __name__ == '__main__':
    while True:
        raw = input('#:')
        command, args = parse_input(raw)
        func = commands.get(command)
        if command is not None:
            command()
        else:
            print('No such command, please try again.')

