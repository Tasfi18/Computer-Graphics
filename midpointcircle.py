import matplotlib.pyplot as plt
import random


def plot_circle_midpoint(r, cx, cy):
    x = 0
    y = r
    p = 1 - r
    marker_size = 3
    while x <= y:
        plt.plot(cx + x, cy + y, 'ro', markersize=marker_size)
        plt.plot(cx + y, cy + x, 'ro', markersize=marker_size)
        plt.plot(cx - x, cy + y, 'ro', markersize=marker_size)
        plt.plot(cx - y, cy + x, 'ro', markersize=marker_size)
        plt.plot(cx - x, cy - y, 'ro', markersize=marker_size)
        plt.plot(cx - y, cy - x, 'ro', markersize=marker_size)
        plt.plot(cx + x, cy - y, 'ro', markersize=marker_size)
        plt.plot(cx + y, cy - x, 'ro', markersize=marker_size)
        if p < 0:
            p = p + 2 * x + 3
        else:
            p = p + 2 * (x - y) + 5
            y -= 1
        x += 1


def main():
    try:
        num_circles = int(input("Enter the number of circles to be drawn: "))
    except ValueError:
        print("Invalid input. Please enter an integer.")
        return

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