f = './data/test.txt'


def read_file():
    file = open(f)
    # skip header row
    next(file)

    num_cities = sum(1 for _ in file)
    print(num_cities)

    lines = open(f).read().splitlines()[1:]
    print('lines', lines)

    distances = read_distances(lines, num_cities)


def read_distances(lines, num_cities):
    # distances = [[None]*num_cities for _ in range(num_cities)]
    # print('dist',distances)
    print(lines)
    x = [read_distances_row(line) for line in lines]
    print('eee', x)
    return x


def read_distances_row(line):
    return line.split(" ")


def create_matrix(data):
    num_cities = sum(1 for _ in data)
    matrix = [[None] * num_cities for _ in range(num_cities)]
    print(num_cities)


create_matrix(read_distances(read_file(), 5))
