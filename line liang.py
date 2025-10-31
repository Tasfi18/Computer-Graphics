import matplotlib.pyplot as plt
import random

def liang_barsky_line_clip(x_min, y_min, x_max, y_max, x1, y1, x2, y2):

    dx = x2 - x1
    dy = y2 - y1

    p = [-dx, dx, -dy, dy]
    q = [x1 - x_min, x_max - x1, y1 - y_min, y_max - y1]

    u1 = 0.0
    u2 = 1.0

    for i in range(4):
        if p[i] == 0:
            if q[i] < 0:
                return None
        else:
            u = q[i] / p[i]
            if p[i] < 0:
                u1 = max(u1, u)
            else:
                u2 = min(u2, u)

    if u1 > u2:
        return None

    x1_clipped = x1 + u1 * dx
    y1_clipped = y1 + u1 * dy
    x2_clipped = x1 + u2 * dx
    y2_clipped = y1 + u2 * dy

    return x1_clipped, y1_clipped, x2_clipped, y2_clipped

def visualize_liang_barsky_line_clipping(x_min, y_min, x_max, y_max, lines):

    plt.figure(figsize=(8, 6))
    plt.title("Liang-Barsky Line Clipping")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")

    # Plot the clipping window
    plt.plot([x_min, x_max, x_max, x_min, x_min], [y_min, y_min, y_max, y_max, y_min], 'r-', label='Clipping Window')

    for x1, y1, x2, y2 in lines:
        # Plot the original line
        plt.plot([x1, x2], [y1, y2], 'b--')  # Removed label
        # Clip the line
        result = liang_barsky_line_clip(x_min, y_min, x_max, y_max, x1, y1, x2, y2)
        if result:
            x1_clip, y1_clip, x2_clip, y2_clip = result
            # Plot the clipped line
            plt.plot([x1_clip, x2_clip], [y1_clip, y2_clip], 'g-')  # Removed label
        else:
            print(f"Line ({x1}, {y1}) to ({x2}, {y2}) is completely outside the clipping window.")

    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # Clipping window coordinates
    x_min, y_min = 100, 100
    x_max, y_max = 300, 300

    # Generate 5 random lines
    num_lines = 5
    lines = []
    for _ in range(num_lines):
        x1 = random.randint(0, 400)  # Adjust range as needed
        y1 = random.randint(0, 400)
        x2 = random.randint(0, 400)
        y2 = random.randint(0, 400)
        lines.append((x1, y1, x2, y2))

    visualize_liang_barsky_line_clipping(x_min, y_min, x_max, y_max, lines)
