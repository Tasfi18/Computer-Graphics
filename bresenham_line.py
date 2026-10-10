import matplotlib.pyplot as plt
import random

from ask import ask_int

def bresenham_line(x1, y1, x2, y2):
    points = []
    
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    if dx > dy:
        p = 2 * dy - dx
        while x1 != x2:
            points.append((x1, y1))
            if p >= 0:
                y1 += sy
                p -= 2 * dx
            p += 2 * dy
            x1 += sx
    else:
        p = 2 * dx - dy
        while y1 != y2:
            points.append((x1, y1))
            if p >= 0:
                x1 += sx
                p -= 2 * dy
            p += 2 * dx
            y1 += sy

    points.append((x2, y2)) 
    return points

def draw_lines(lines):
    plt.figure(figsize=(8, 8))
    for x1, y1, x2, y2 in lines:
        points = bresenham_line(x1, y1, x2, y2)
        x_vals, y_vals = zip(*points)
        plt.plot(x_vals, y_vals, color='green')  

    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Bresenham's Line Algorithm Visualization")
    plt.gca().set_aspect('equal', adjustable='box')

    plt.show()

if __name__ == "__main__":
    num_lines = ask_int("Enter the number of lines: ", minimum=1)
    lines = []
    for _ in range(num_lines):
        x1 = random.randint(1, 10)
        y1 = random.randint(1, 10)
        x2 = random.randint(15, 30)
        y2 = random.randint(15, 30)
        lines.append((x1, y1, x2, y2))

    draw_lines(lines)
