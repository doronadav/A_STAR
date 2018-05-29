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
        self.open_dict = dict()
        self.open_heap = dict()
        self.open_list_length = 1
        self.suspected_goal = None

    def heuristic_func(self, board):
        return sum(abs((val - 1) % N - i % N) + abs((val - 1) // N - i // N) for i, val in enumerate(board) if val)

    def search_late_goal_test(self, start, goal):
        # For our case we must put a tuple in the queue to make sure
        # the get will return the state (board) with the smallest f.
        fifo_queue_index = 0
        start_data = [self.heuristic_func(start.value), fifo_queue_index, start, None]
        self.open_dict = {start: start_data}
        self.open_heap = [start_data]

        while self.open_heap:
            current_data = heapq.heappop(self.open_heap)
            _, _, current, _ = current_data

            if current.value == goal:
                return current, self.open_list_length

            del self.open_dict[current]
            self.closed_dict[current] = 1

            for neighbor in current.calc_children():
                if neighbor in self.closed_dict:
                    continue

                h_val = self.h_dict.get(neighbor, None)
                if h_val is None:
                    h_val = self.heuristic_func(neighbor.value)
                    self.h_dict[neighbor] = h_val
                f = neighbor.g + h_val
                fifo_queue_index += 1
                neighbor_data = [f, fifo_queue_index, neighbor, current_data]

                if neighbor not in self.open_dict:
                    self.open_dict[neighbor] = neighbor_data
                    heapq.heappush(self.open_heap, neighbor_data)
                    self.open_list_length += 1
                else:
                    old_neighbor_data = self.open_dict[neighbor]
                    if neighbor_data < old_neighbor_data:
                        old_neighbor_data[:] = neighbor_data
                        heapq.heapify(self.open_heap)
        else:
            start.path = []
            return 'Board: {}  is not a valid board'.format(start)

    def search_early_goal_test(self, start, goal):
        fifo_queue_index = 0
        start_data = [self.heuristic_func(start.value), fifo_queue_index, start, None]
        self.open_dict = {start: start_data}
        self.open_heap = [start_data]
        while self.open_heap:
            current_data = heapq.heappop(self.open_heap)
            _, _, current, _ = current_data

            if current.value == goal:
                return current, self.open_list_length

            del self.open_dict[current]
            self.closed_dict[current] = 1

            for neighbor in current.calc_children():
                if neighbor in self.closed_dict:
                    continue

                if neighbor.value == goal:  # Early goal test
                    if self.suspected_goal is None or neighbor.g < self.suspected_goal.g:
                        self.suspected_goal = neighbor

                h_val = self.h_dict.get(neighbor, None)
                if h_val is None:
                    h_val = self.heuristic_func(neighbor.value)
                    self.h_dict[neighbor] = h_val
                f = neighbor.g + h_val
                if self.suspected_goal is not None and id(self.suspected_goal)!=id(neighbor) and not f < self.suspected_goal.g:
                    continue    # Early goal test - found a smaller path to goal not inserting neighbour to open list.
                fifo_queue_index += 1
                neighbor_data = [f, fifo_queue_index, neighbor, current_data]

                if neighbor not in self.open_dict:
                    self.open_dict[neighbor] = neighbor_data
                    heapq.heappush(self.open_heap, neighbor_data)
                    self.open_list_length += 1
                else:
                    old_neighbor_data = self.open_dict[neighbor]
                    if neighbor_data < old_neighbor_data:
                        old_neighbor_data[:] = neighbor_data
                        heapq.heapify(self.open_heap)
        else:
            start.path = []
            return 'Board: {}  is not a valid board'.format(start)
