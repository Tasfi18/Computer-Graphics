import matplotlib.pyplot as plt
import random

def plot_circle_points(xc, yc, x, y, points):
    """Utilizes 8-way symmetry to plot circle points"""
    points.extend([
        (xc + x, yc + y), (xc - x, yc + y),
        (xc + x, yc - y), (xc - x, yc - y),
        (xc + y, yc + x), (xc - y, yc + x),
        (xc + y, yc - x), (xc - y, yc - x)
    ])

def bresenham_circle(xc, yc, r):
    """Implements Bresenham's Circle Algorithm"""
    x, y = 0, r
    d = 3 - 2 * r 
    points = []

    while x <= y:
        plot_circle_points(xc, yc, x, y, points)
        x += 1
        if d < 0:
            d = d + 4 * x + 6
        else:
            y -= 1
            d = d + 4 * (x - y) + 10

    return points

def draw_multiple_circles(circle_data):
    """Draws multiple circles on the same plot"""
    plt.figure(figsize=(8, 8))

    for xc, yc, r in circle_data:
        points = bresenham_circle(xc, yc, r)
        x_vals, y_vals = zip(*points)
        plt.scatter(x_vals, y_vals, s=10, label=f"Circle({xc}, {yc}, {r})")  

    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True)
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Bresenham's Circle Algorithm - Multiple Circles")
    plt.legend()
    plt.show()


num_circles = int(input("Enter the number of circles: "))


circle_list = []
for _ in range(num_circles):
    xc = random.randint(100, 900)  
    yc = random.randint(100, 900)  
    r = random.randint(20, 100)    
    circle_list.append((xc, yc, r))


draw_multiple_circles(circle_list)
