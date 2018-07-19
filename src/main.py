import os
import sys
import time

from src.a_star import AStar, State, N

dir_path = os.path.dirname(os.path.realpath(__file__))


def main():
    file_path = dir_path + '/1.d'
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)
    try:
        output = open("bla-hadar.output", "w")
        # output = open("A_Star_Output_late_goal_test.output", "w")
        output.write('Staring calculation:\n')
        with open(file_path, "r") as states_file:
            index = 0
            for line in states_file:
                index = index + 1
                line_list = line.split()
                output.write('Board number {} is: {}\n'.format(index, line_list))
                # print line_list

                source = State(value=map(int, line_list), blank_index=line_list.index("0"), parent=None)

                algo = AStar()
                start = time.time()
                res_board, open_list_size = algo.search_early_goal_test(source, goal)
                # res_board, open_list_size = algo.search_late_goal_test(source, goal)
                end = time.time()
                output.write('Goal Found! Length of path: {} \n'.format(len(res_board.path)))
                # output.write('Path to goal is : {}\n'.format(res_board.path))
                output.write('Time it took to calculate board num {} is: {} seconds\n'.format(index, end - start))
                output.write('Size of open list is: {}\n'.format(open_list_size))
                print 'Finished board number {}, open list size was: {}'.format(index, open_list_size)
        output.close()
    except Exception as e:
        print e.message


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print e.message
        sys.exit(1)
    sys.exit(0)
