import matplotlib.pyplot as plt

from ask import ask_int

def dda_algorithm(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    steps = max(abs(dx), abs(dy))
    if steps == 0:  # both ends are the same point
        return [round(x1)], [round(y1)]

    x_inc = dx / steps
    y_inc = dy / steps

    x, y = x1, y1

    x_points = []
    y_points = []

    for _ in range(int(steps) + 1):
        x_points.append(round(x))
        y_points.append(round(y))
        x += x_inc
        y += y_inc

    return x_points, y_points

def draw_line(x1, y1, x2, y2):
    x_points, y_points = dda_algorithm(x1, y1, x2, y2)

    plt.plot(x_points, y_points, marker="o", color="blue", markersize=5)
    plt.grid(True)
    plt.xlim(min(x1, x2) - 5, max(x1, x2) + 5)
    plt.ylim(min(y1, y2) - 5, max(y1, y2) + 5)
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("DDA Line Drawing Algorithm")
    plt.show()

if __name__ == "__main__":
    x1 = ask_int("Enter x1: ")
    y1 = ask_int("Enter y1: ")
    x2 = ask_int("Enter x2: ")
    y2 = ask_int("Enter y2: ")
    draw_line(x1, y1, x2, y2)
