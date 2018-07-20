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
        self.h = self.calc_heuristic()
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

    def calc_heuristic(self):
        return sum(abs((val - 1) % N - i % N) + abs((val - 1) // N - i // N) for i, val in enumerate(self.value) if val)


class AStar:

    def __init__(self):
        self.h_dict = dict()
        self.closed_dict = dict()
        self.open_dict = dict()
        self.open_heap = dict()
        self.open_list_length = 1
        self.suspected_goal = None

    # def heuristic_func(self, board):
    #     return sum(abs((val - 1) % N - i % N) + abs((val - 1) // N - i // N) for i, val in enumerate(board) if val)
    #
    def search_late_goal_test(self, start, goal):
        # For our case we must put a tuple in the queue to make sure
        # the get will return the state (board) with the smallest f.
        #fifo_index = 0
        start_data = [start.h, 0, str(start.value)]
        # start_data = [start.h, 0, fifo_index, str(start.value)]
        self.open_dict = {str(start.value): start}
        self.open_heap = [start_data]
        try:
            while self.open_heap:
                current_data = heapq.heappop(self.open_heap)
                _, _, key = current_data
                # _, _, _, key = current_data
                current = self.open_dict.get(key)
                if current is None:
                    continue

                if current.value == goal:
                    return current, self.open_list_length

                del self.open_dict[key]
                self.closed_dict[key] = 1

                for neighbor in current.calc_children():
                    key_neighbor = str(neighbor.value)
                    if key_neighbor in self.closed_dict:
                        continue

                    # fifo_index += 1
                    f = neighbor.g + neighbor.h
                    neighbor_data = [f, neighbor.h, key_neighbor] # fifo_index % 20 instead of g
                    # neighbor_data = [f, neighbor.h, fifo_index, key_neighbor]

                    if key_neighbor not in self.open_dict:
                        self.open_dict[key_neighbor] = neighbor
                        heapq.heappush(self.open_heap, neighbor_data)
                        self.open_list_length += 1
                    else:
                        old_neighbor = self.open_dict[key_neighbor]
                        if neighbor.g < old_neighbor.g:
                            self.open_dict[key_neighbor] = neighbor
                            heapq.heappush(self.open_heap, neighbor_data)
                            self.open_list_length += 1

            else:
                start.path = []
                return 'Board: {}  is not a valid board'.format(start)
        except Exception as e:
            print e.message

    def search_early_goal_test(self, start, goal):
        # fifo_index = 0
        skipped_nodes = 0
        start_data = [start.h, 0, str(start.value)]
        # start_data = [start.h, 0, fifo_index, str(start.value)]
        self.open_dict = {str(start.value): start}
        self.open_heap = [start_data]
        try:
            while self.open_heap:
                current_data = heapq.heappop(self.open_heap)
                _, _, key = current_data
                # _, _, _, key = current_data
                current = self.open_dict.get(key)
                if current is None:
                    continue

                if current.value == goal:
                    print skipped_nodes
                    return current, self.open_list_length

                del self.open_dict[key]
                self.closed_dict[key] = 1

                for neighbor in current.calc_children():
                    if str(neighbor.value) in self.closed_dict:
                        continue

                    if neighbor.value == goal:  # Early goal test
                        if self.suspected_goal is None or neighbor.g < self.suspected_goal.g:
                            self.suspected_goal = neighbor
                            print 'suspected goal is {} with f: {}'.format(neighbor.value, neighbor.g)
                            #print self.open_heap
                        else:
                            print 'skipped bigger goal state {} with f: {}'.format(neighbor.value, neighbor.g)
                            skipped_nodes += 1
                            continue

                    f = neighbor.g + neighbor.h
                    if self.suspected_goal is not None and id(self.suspected_goal)!=id(neighbor) and not f < self.suspected_goal.g:
                        print 'skiped state {} with f {}'.format(neighbor.value, f)
                        skipped_nodes += 1
                        continue

                    #fifo_index += 1
                    key_neighbor = str(neighbor.value)
                    neighbor_data = [f, neighbor.g, key_neighbor] # fifo_index % 20
                    # neighbor_data = [f, neighbor.h, fifo_index, key_neighbor]

                    if key_neighbor not in self.open_dict:
                        self.open_dict[key_neighbor] = neighbor
                        heapq.heappush(self.open_heap, neighbor_data)
                        self.open_list_length += 1

                    else:
                        old_neighbor = self.open_dict[key_neighbor]
                        if neighbor.g < old_neighbor.g:
                            self.open_dict[key_neighbor] = neighbor
                            heapq.heappush(self.open_heap, neighbor_data)
                            self.open_list_length += 1

            else:
                start.path = []
                return 'Board: {}  is not a valid board'.format(start)
        except Exception as e:
            print e.message
