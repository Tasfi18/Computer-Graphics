import matplotlib.pyplot as plt
import random

from ask import ask_int


def midpoint_circle_points(r, cx, cy):
    """Midpoint circle algorithm: the points of one octant, mirrored to all eight."""
    points = []
    x = 0
    y = r
    p = 1 - r
    while x <= y:
        points.extend([
            (cx + x, cy + y), (cx + y, cy + x), (cx - x, cy + y), (cx - y, cy + x),
            (cx - x, cy - y), (cx - y, cy - x), (cx + x, cy - y), (cx + y, cy - x),
        ])
        if p < 0:
            p = p + 2 * x + 3
        else:
            p = p + 2 * (x - y) + 5
            y -= 1
        x += 1
    return points


def plot_circle_midpoint(r, cx, cy):
    xs, ys = zip(*midpoint_circle_points(r, cx, cy))
    plt.plot(xs, ys, 'ro', markersize=3)


def main():
    num_circles = ask_int("Enter the number of circles to be drawn: ", minimum=1)

    center_range = (-50, 50)  
    radius_range = (5, 30)  

    for i in range(num_circles):
    
        cx = random.randint(*center_range)
        cy = random.randint(*center_range)
        r = random.randint(*radius_range)
        print(f"Drawing circle {i + 1}: Center=({cx}, {cy}), Radius={r}")
        plot_circle_midpoint(r, cx, cy)

    plt.axhline(0, color='black', linewidth=2)
    plt.axvline(0, color='black', linewidth=2)

    plt.xlim(-100, 100)
    plt.ylim(-100, 100)

    plt.title("Random Circles using Midpoint Circle Algorithm")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()