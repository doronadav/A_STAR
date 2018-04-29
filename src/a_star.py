from Queue import PriorityQueue
from copy import deepcopy

N = 2


def can_move_left(index):
    return not index % N == 0


def can_move_right(index):
    return not index % N == N - 1


def can_move_up(index):
    return not index / N == 0


def can_move_down(index):
    return not index / N == N - 1


def manhattan(board):
    return sum(abs((val - 1) % N - i % N) + abs((val - 1) // N - i // N) for i, val in enumerate(board) if val)


class State(object):
    def __init__(self, value, parent, g=0):
        self.children = []
        self.parent = parent
        self.value = value              # list representing the board
        if parent:
            self.path = parent.path[:]
            self.path.append(value)
            self.g = self.parent.g + 1
        else:
            self.g = g
            self.path = [value]

    def calc_children(self):
        [index_0] = [i for i, val in enumerate(self.value) if not val]
        if can_move_left(index_0):
            new_board = deepcopy(self.value)
            new_board[index_0], new_board[index_0 - 1] = new_board[index_0 - 1], new_board[index_0]
            self.children.append(State(value=new_board, parent=self))
        if can_move_right(index_0):
            new_board = deepcopy(self.value)
            new_board[index_0], new_board[index_0 + 1] = new_board[index_0 + 1], new_board[index_0]
            self.children.append(State(value=new_board, parent=self))
        if can_move_up(index_0):
            new_board = deepcopy(self.value)
            new_board[index_0], new_board[index_0 - N] = new_board[index_0 - N], new_board[index_0]
            self.children.append(State(value=new_board, parent=self))
        if can_move_down(index_0):
            new_board = deepcopy(self.value)
            new_board[index_0], new_board[index_0 + N] = new_board[index_0 + N], new_board[index_0]
            self.children.append(State(value=new_board, parent=self))


class AStar:

    def __init__(self):
        self.n = N
        self.open_list = PriorityQueue()
        self.closed_list = []

    def heuristic_func(self, node):
        return manhattan(node)

    def a_star(self, source, goal):
        current = source

        # For our case we must put a tuple in the queue to make sure
        # the get will return the state (board) with the smallest f.
        self.open_list.put((0, current))

        while not self.open_list.empty():
            _, current = self.open_list.get()
            if current.value == goal:
                return current

            current.calc_children()
            for neighbor in current.children:
                if neighbor.value in self.closed_list:
                    continue
                h = self.heuristic_func(neighbor.value)
                f = neighbor.g + h
                print 'inserting ({}) to queue with f: {} and h: {}'.format(neighbor.value, f, h)
                self.open_list.put((f, neighbor))
            self.closed_list.append(current.value)
        else:
            source.path = []
            return 'Board: {}  is not a valid board'.format(source.value)
