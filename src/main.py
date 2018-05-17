import os
import sys
import time

from src.a_star import AStar, State, N

dir_path = os.path.dirname(os.path.realpath(__file__))


def main():
    file_path = dir_path + '/states15_b.d'
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)
    try:
        with open(file_path, "r") as states_file:
            for line in states_file:
                line_list = line.split()
                print line_list

                source = State(value=map(int, line_list), blank_index=line_list.index("0"), parent=None)

                start = time.time()
                algo = AStar()
                res = algo.a_star(source, goal)
                end = time.time()
                print 'Path is : {} ' \
                      '\nLentgh of path: {}'.format(res.path, len(res.path))
                print end - start
    except Exception as e:
        print e.message




# def main():
#     file_path = dir_path + '/states15_b.d'
#
#     try:
#         with open(file_path, "r") as states_file:
#             for line in states_file:
#                 line_list = line.split()
#                 print line_list
#     except Exception as e:
#         print e.message
#
#     # goal = []
#     # for i in range(N * N - 1):
#     #     goal.append(i + 1)
#     # goal.append(0)
#     start =time.time()
#     #goal = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)
#     goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
#     source = State(value=[2, 0, 3, 7, 8, 5,1,4,6], blank_index=1, parent=None)
#     #goal = [1, 2, 3, 0]
#     #source = State(value=[3, 1, 0, 2], parent=None)
#     #source = State(value=[11, 0, 4,7,2, 15,1, 8,5, 14, 9,3, 13,6, 12, 10 ], blank_index=1, parent=None) #2.47 sec, path:40 puzzle:39
#
#     #source = State(value=[2, 9,3,5,8, 11, 12,  7,15,  4,  0, 13, 6,  1, 10, 14 ], blank_index=10, parent=None) # takes 330 seconds, Length = 51 puzzle50
#     #source = State(value=[2, 9, 6, 8, 14, 0, 3, 15, 4, 1, 12, 11, 5, 7, 10, 13], parent=None)
#     #source = State(value=[1, 2, 0, 4, 13, 5, 6, 3, 8, 7, 11, 9, 14, 15, 10, 12], parent=None)
#     #source = State(value=[13,1, 10,4, 8, 12,6, 3,15,9, 5, 14,0, 7,  2, 11], blank_index=12, parent=None)
#     algo = AStar()
#     res = algo.a_star(source, goal)
#     end = time.time()
#     print 'Path is : {} ' \
#           '\nLentgh of path: {}'.format(res.path, len(res.path))
#     print end-start

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print e.message
        sys.exit(1)
    sys.exit(0)
