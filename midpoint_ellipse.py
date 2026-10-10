import matplotlib.pyplot as plt
import math
import random

from ask import ask_int

def midpoint_ellipse(center_x, center_y, rx, ry):
    x = 0
    y = ry
    rx_sq = rx * rx
    ry_sq = ry * ry
    two_rx_sq = 2 * rx_sq
    two_ry_sq = 2 * ry_sq
    px = 0
    py = two_rx_sq * y

    ellipse_points = []

    p1 = ry_sq - rx_sq * ry + 0.25 * rx_sq
    while px < py:
        ellipse_points.extend([
            (center_x + x, center_y + y),
            (center_x - x, center_y + y),
            (center_x + x, center_y - y),
            (center_x - x, center_y - y)
        ])
        x += 1
        px += two_ry_sq
        if p1 < 0:
            p1 += two_ry_sq * x + ry_sq
        else:
            y -= 1
            py -= two_rx_sq
            p1 += two_ry_sq * x - two_rx_sq * y + ry_sq

    p2 = ry_sq * (x + 0.5)**2 + rx_sq * (y - 1)**2 - rx_sq * ry_sq
    while y >= 0:
        ellipse_points.extend([
            (center_x + x, center_y + y),
            (center_x - x, center_y + y),
            (center_x + x, center_y - y),
            (center_x - x, center_y - y)
        ])
        y -= 1
        py -= two_rx_sq
        if p2 > 0:
            p2 += rx_sq - two_rx_sq * y
        else:
            x += 1
            px += two_ry_sq
            p2 += two_ry_sq * x - two_rx_sq * y + rx_sq

    return list(set(ellipse_points))

if __name__ == "__main__":
    num_ellipses = ask_int("Enter the number of ellipses to draw: ", minimum=1)

    plt.figure(figsize=(8, 6))
    
    for i in range(num_ellipses):
        # Get ellipse parameters (you can customize how you get these)
        center_x = ask_int(f"Enter center x for ellipse {i+1}: ")
        center_y = ask_int(f"Enter center y for ellipse {i+1}: ")
        radius_x = ask_int(f"Enter x-radius for ellipse {i+1}: ", minimum=1)
        radius_y = ask_int(f"Enter y-radius for ellipse {i+1}: ", minimum=1)

        points = midpoint_ellipse(center_x, center_y, radius_x, radius_y)

        # Sort points based on angle around the center (approximate)
        def angle(point):
            return math.atan2(point[1] - center_y, point[0] - center_x)

        sorted_points = sorted(points, key=angle)

        x_coords = [p[0] for p in sorted_points]
        y_coords = [p[1] for p in sorted_points]

        # Plot the ellipse as a continuous line
        x_coords.append(x_coords[0])  # close the outline
        y_coords.append(y_coords[0])
        plt.plot(x_coords, y_coords, label=f"Ellipse {i+1}: centre ({center_x}, {center_y}), radii {radius_x} x {radius_y}")
        plt.scatter(center_x, center_y, color='red', marker='o')

    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Midpoint Ellipse Algorithm - Multiple Ellipses")
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True)
    plt.legend()
    plt.show()