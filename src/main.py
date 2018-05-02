import os
import sys

from src.a_star import AStar, State, N

dir_path = os.path.dirname(os.path.realpath(__file__))

def main():
    # file_path = dir_path + '/states15.d'
    #
    # try:
    #     with open(file_path, "r") as states_file:
    #         for line in states_file:
    #             line_list = line.split()
    #             print line_list
    # except Exception as e:
    #     print e.message

    # goal = []
    # for i in range(N * N - 1):
    #     goal.append(i + 1)
    # goal.append(0)

    goal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
    # goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    # source = State(value=[2, 3, 8, 5, 6, 4, 1, 0, 7], parent=None)
    # source = State(value=[3, 0, 1, 2], parent=None)
    source = State(value=[14, 13, 15, 7, 11, 12, 9, 5, 6, 0, 2, 1, 4, 8, 10, 3], parent=None)
    # source = State(value=[2, 9, 6, 8, 14, 0, 3, 15, 4, 1, 12, 11, 5, 7, 10, 13], parent=None)
    # source = State(value=[13, 5, 4, 10, 9, 12, 8, 14, 2, 3, 7, 1, 0, 15, 11, 6], parent=None)
    algo = AStar()
    res = algo.a_star(source, goal)
    print 'Path is : {} ' \
          '\nLentgh of path: {}'.format(res.path, len(res.path))

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print e.message
        sys.exit(1)
    sys.exit(0)
