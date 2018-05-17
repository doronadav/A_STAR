from Queue import PriorityQueue
from copy import deepcopy
import heapq

N = 4


def can_move_left(index):
    return not index % N == 0


def can_move_right(index):
    return not index % N == N - 1


def can_move_up(index):
    return not index / N == 0


def can_move_down(index):
    return not index / N == N - 1

class State(object):
    def __init__(self, value, parent, blank_index, g=0):
        self.children = []
        self.parent = parent
        self.value = tuple(value)              # list representing the board
        self.closed = False
        self.blank_index = blank_index
        if parent:
            self.path = parent.path[:]
            self.path.append(value)
            self.g = self.parent.g + 1
        else:
            self.g = g
            self.path = [value]

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def calc_children(self):
        #[index_0] = [i for i, val in enumerate(self.value) if not val]
        if can_move_left(self.blank_index):
            new_board = list(self.value)
            new_board[self.blank_index], new_board[self.blank_index - 1] = new_board[self.blank_index - 1], new_board[self.blank_index]
            yield State(value=new_board, blank_index=self.blank_index-1, parent=self)
        if can_move_right(self.blank_index):
            new_board = list(self.value)
            new_board[self.blank_index], new_board[self.blank_index + 1] = new_board[self.blank_index + 1], new_board[self.blank_index]
            yield State(value=new_board,blank_index=self.blank_index+1, parent=self)
        if can_move_up(self.blank_index):
            new_board = list(self.value)
            new_board[self.blank_index], new_board[self.blank_index - N] = new_board[self.blank_index - N], new_board[self.blank_index]
            yield State(value=new_board, blank_index=self.blank_index-N, parent=self)
        if can_move_down(self.blank_index):
            new_board = list(self.value)
            new_board[self.blank_index], new_board[self.blank_index + N] = new_board[self.blank_index + N], new_board[self.blank_index]
            yield State(value=new_board, blank_index=self.blank_index+N, parent=self)


class AStar:

    def __init__(self):
        self.h_dict = dict()
        self.closed_dict = dict()
        self.open_list_length = 1

    def heuristic_func(self, board):
        return sum(abs((val - 1) % N - i % N) + abs((val - 1) // N - i // N) for i, val in enumerate(board) if val)

    def a_star(self, start, goal):

        # For our case we must put a tuple in the queue to make sure
        # the get will return the state (board) with the smallest f.
        start_data = [self.heuristic_func(start.value), 0, start, None]
        self.open_dict = {start: start_data}
        self.open_heap = [start_data]

        while self.open_heap:
            current_data = heapq.heappop(self.open_heap)
            f_curr, g_curr, current, parent_data = current_data

            if current.value == goal:
                print "Open list length {}".format(self.open_list_length)
                return current

            del self.open_dict[current]
            self.closed_dict[current] = 1
            # if current.closed or str(current.value) in self.closed_dict:
            #    continue

            for neighbor in current.calc_children():
                #neighbor_str = str(neighbor.value)
                if neighbor in self.closed_dict:
                    continue

                h_val = self.h_dict.get(neighbor, None)
                if h_val is None:
                    h_val = self.heuristic_func(neighbor.value)
                    self.h_dict[neighbor] = h_val
                f = neighbor.g + h_val
                neighbor_data = [f, neighbor.g, neighbor, current_data]

                if neighbor not in self.open_dict:
                    self.open_dict[neighbor] = neighbor_data
                    heapq.heappush(self.open_heap, neighbor_data)
                    self.open_list_length += 1
                    #print "insert node {} with f {},  h {}".format(neighbor.value, f, h_val)
                else:
                    old_neighbor_data = self.open_dict[neighbor]
                    if neighbor_data < old_neighbor_data:
                        old_neighbor_data[:] = neighbor_data
                        heapq.heapify(self.open_dict)


        #         val = self.open_dict.get(neighbor, None)
        #         if val is None:
        #             # case 1 - first insertion
        #             heapq.heappush(self.open_heap, (f, neighbor.g, neighbor))
        #             self.open_dict[neighbor] = neighbor
        #         elif val.g > neighbor.g:
        #             val.closed = True
        #             self.open_dict[neighbor_str] = neighbor
        #             heapq.heappush(self.open_heap, (f, neighbor.g, neighbor))
        #         print "inserting to open list {} with h {}".format(, h_val)
        #
        #     current.closed = True
        #     self.closed_dict[str(current.value)] = 1
        #     self.open_dict.pop(str(current.value))
        else:
            start.path = []
            return 'Board: {}  is not a valid board'.format(start)