from Queue import PriorityQueue
from copy import deepcopy

N = 4


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
        self.closed_dict = dict()
        self.uniqueness_dict = dict()

    def heuristic_func(self, node):
        return manhattan(node)

    def a_star(self, source, goal):
        current = source

        # For our case we must put a tuple in the queue to make sure
        # the get will return the state (board) with the smallest f.
        self.open_list.put((0, current))
        self.uniqueness_dict[str(current.value)] = current

        while not self.open_list.empty():
            _, current = self.open_list.get()

            if current.value == goal:
                return current

            current.calc_children()
            for neighbor in current.children:
                if self.closed_dict.has_key(str(neighbor.value)):
                # if neighbor.value in self.closed_list:
                    continue
                h = self.heuristic_func(neighbor.value)
                f = neighbor.g + h
                # self.open_list.put((f, neighbor))
                val = self.uniqueness_dict.get(str(neighbor.value), None)
                if val is None:
                    # case 1 - first insertion
                    self.open_list.put((f, neighbor))
                    self.uniqueness_dict[str(neighbor.value)] = neighbor
                    print 'inserted {} with heuristic_func: {}'.format(neighbor.value, h)
                elif val.g < neighbor.g:
                    self.update_open_list_state(f, neighbor)

            self.closed_dict[str(current.value)] = 1
            # self.closed_list.append(current.value)
            self.uniqueness_dict.pop(str(current.value))
        else:
            source.path = []
            return 'Board: {}  is not a valid board'.format(source.value)

    def update_open_list_state(self, new_f, new_state):
        res = []
        while not self.open_list.empty():
            priority, state = self.open_list.get()
            if state.value == new_state.value:
                if new_f < priority:
                    self.open_list.put((new_f, new_state))
                else:
                    self.open_list.put((priority, state))
                for p, s in res:
                    self.open_list.put((p, s))
                return
            else:
                res.append((priority, state))
