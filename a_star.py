from Queue import PriorityQueue
import math


class State(object):
    def __init__(self, value, parent, start=0, goal=0, solver=0):
        self.children = []
        self.parent = parent
        self.value = value
        self.dist = 0
        if parent:
            self.path = parent.path[:]
            self.path.append(value)
            self.start = parent.start
            self.goal = parent.goal
        else:
            self.path = [value]
            self.start = start
            self.goal = goal

    def create_neighbors(self):
        pass

    def get_dist(self):
        pass

    def get_neighbors(self):
        pass


class Node(object):

    neighbors = list()

    def __init__(self, cost, value, neighbors):
        self.g = cost
        self.h = 0
        self.value = value
        self.neighbors.add(neighbors)


class Heruristic:

    @staticmethod
    def HeuristicFactory(type, node, goal):
        if type == "manhatten":
            return Heruristic.manhattan(node, goal)
        elif type == 'air_distance':
            return Heruristic.air_distance(node, goal)

    @staticmethod
    def manhattan(node, goal):
        return abs(goal.x - node.x) + abs(goal.y - node.y)

    @staticmethod
    def air_distance(node, goal):
        return math.sqrt(pow(node.x - goal.x, 2) + pow(node.y - goal.y, 2))


class AStar:

    def __init__(self, h_func):
        self.open_list = PriorityQueue()
        self.closed_list = []
        self.heuristic_func = h_func

    def print_path(self):
        pass

    def heuristic_func(self, node, goal):
        return Heruristic.HeruristicFactoty(node, goal, self.heuristic_func)

    # def late_goal_test(self, state, goal, f, cost):
    #     if state == goal:
    #         cost = state.g
    #         if cost < 0 or f < cost:
    #             return True
    #     return False

    def a_star(self, source, goal, grid, algo_type=0):
        current = source
        cost = -1

        self.open_list.put(current, 0)

        while not self.open_list.empty():
            current = self.open_list.get()
            if current == goal:
                return self.print_path(current)

            self.open_list.remove(current)
            self.closed_list.append(current)

            for neighbor in current.get_neighbors():
                if neighbor in self.closed_list:
                    continue
                f = neighbor.g + self.heuristic_func(neighbor, goal)
                self.open_list.put(neighbor, f)


            self.closed_list.append(current)
