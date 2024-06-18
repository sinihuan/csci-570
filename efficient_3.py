import os
import time
import psutil

def read_input():
    with open('input.txt') as file:
        file_lines = file.readlines()
        x = file_lines[0].strip()
        x_step = 0
        for line in file_lines[1:]:
            try:
                int_value = int(line.strip())
                x_step += 1
            except ValueError:
                break

        y_line = x_step+2
        y = file_lines[y_line-1].strip()
        all_lines = len(file_lines)

        for i in range(1, x_step + 1):
            insert_loc = int(file_lines[i].strip())+1
            x = x[:insert_loc] + x + x[insert_loc:]

        for j in range(y_line, all_lines):
            insert_loc = int(file_lines[j].strip())+1
            y = y[:insert_loc] + y + y[insert_loc:]

    return x, y


def result(OPT, x, y, m, n, alpha, delta):
    x_result = ''
    y_result = ''
    i, j = n, m
    while i > 0 and j > 0:
        if OPT[i][j] == OPT[i-1][j-1] + alpha[x[j-1]][y[i-1]]:
            y_result = y[i-1] + y_result
            x_result = x[j-1] + x_result
            i -= 1
            j -= 1
        elif OPT[i][j] == OPT[i - 1][j] + delta:
            y_result = y[i - 1] + y_result
            x_result = '_' + x_result
            i -= 1
        else:
            y_result = '_' + y_result
            x_result = x[j - 1] + x_result
            j -= 1

    while i > 0:
        y_result = y[i - 1] + y_result
        x_result = '_' + x_result
        i -= 1

    while j > 0:
        y_result = '_' + y_result
        x_result = x[j - 1] + x_result
        j -= 1

    return x_result, y_result


def Compute_OPT(x, y, alpha, delta):
    n = len(y)
    m = len(x)

    OPT = [ [0 for j in range(m+1)] for i in range(n+1)]

    # Initialize col0 and row0
    for i in range(n+1):
        OPT[i][0] = i * delta
    for j in range(m+1):
        OPT[0][j] = j * delta

    # Recursion Formula
    for i in range(1, n+1):
        for j in range(1, m+1):
            OPT[i][j] = min(OPT[i-1][j-1] + alpha[x[j-1]][y[i-1]],
                            OPT[i-1][j] + delta,
                            OPT[i][j-1] + delta)
    final_value = OPT[n][m]

    x_result, y_result = result(OPT, x, y, m, n, alpha, delta)

    return final_value, x_result, y_result


def find_split(x, y, alpha, delta):
    m = len(x)
    n = len(y)

    OPT = [[0 for _ in range(m+1)] for _ in range(2)]

    for j in range(m+1):
        OPT[0][j] = delta * j

    for i in range(1, n+1):
        OPT[1][0] = i * delta
        for j in range(1, m+1):
            OPT[1][j] = min(OPT[0][j - 1] + alpha[x[j - 1]][y[i - 1]],
                            OPT[0][j] + delta,
                            OPT[1][j - 1] + delta)

        for j in range(0, m):
            OPT[0][j] = OPT[1][j]

    return OPT[-1]

def divide_conquer(x, y, alpha, delta):
    n = len(y)
    m = len(x)

    if m <= 2 or n <= 2:
        return Compute_OPT(x, y, alpha, delta)

    y_left = y[:n//2]
    y_right = y[n//2:]

    min_opt = float('inf')
    split_point = float('inf')

    opt_left = find_split(x, y_left, alpha, delta)
    opt_right = find_split(x[::-1], y_right[::-1], alpha, delta)[::-1]

    for i in range(len(opt_right)):
        s = opt_left[i] + opt_right[i]
        if s <= min_opt:
            min_opt = s
            split_point = i

    x_left = x[:split_point]
    x_right = x[split_point:]

    _, x_left_final, y_left_final = divide_conquer(x_left, y_left, alpha, delta)
    _, x_right_final, y_right_final = divide_conquer(x_right, y_right, alpha, delta)

    return min_opt, x_left_final + x_right_final, y_left_final + y_right_final


def main():
    delta = 30
    alpha = {
        'A': {'A': 0, 'C': 110, 'G': 48, 'T': 94},
        'C': {'A': 110, 'C': 0, 'G': 118, 'T': 48},
        'G': {'A': 48, 'C': 118, 'G': 0, 'T': 110},
        'T': {'A': 94, 'C': 48, 'G': 110, 'T': 0},
    }
    x, y = read_input()

    # Time
    start_time = time.time()
    final_value, x_result, y_result = divide_conquer(x, y, alpha, delta)
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000

    # Memory
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)

    # Check if output file exists, create it if not
    output_file = 'output.txt'
    if not os.path.exists(output_file):
        with open(output_file, 'w') as file:
            pass  # Create an empty file

    # Write results to the output file
    with open(output_file, 'w') as file:
        file.write(str(final_value) + '\n')  # Convert final_value to string
        file.write(x_result + '\n')
        file.write(y_result + '\n')
        file.write(str(time_taken) + '\n')
        file.write(str(memory_consumed) + '\n')

main()