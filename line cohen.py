import matplotlib.pyplot as plt
import random

def cohen_sutherland_line_clip(x_min, y_min, x_max, y_max, x1, y1, x2, y2):

    INSIDE = 0    # 0000
    LEFT = 1      # 0001
    RIGHT = 2     # 0010
    BOTTOM = 4    # 0100
    TOP = 8       # 1000

    def compute_region_code(x, y):
        code = INSIDE
        if x < x_min:
            code |= LEFT
        elif x > x_max:
            code |= RIGHT
        if y < y_min:
            code |= BOTTOM
        elif y > y_max:
            code |= TOP
        return code

    code1 = compute_region_code(x1, y1)
    code2 = compute_region_code(x2, y2)
    accept = False

    while True:
        if code1 == 0 and code2 == 0:
            accept = True
            break
        elif (code1 & code2) != 0:
            return None
        else:
            outcode = code1 if code1 != 0 else code2
            x, y = 0, 0

            if outcode & TOP:
                x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                y = y_max
            elif outcode & BOTTOM:
                x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                y = y_min
            elif outcode & RIGHT:
                y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                x = x_max
            elif outcode & LEFT:
                y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                x = x_min

            if outcode == code1:
                x1, y1 = x, y
                code1 = compute_region_code(x1, y1)
            else:
                x2, y2 = x, y
                code2 = compute_region_code(x2, y2)

    if accept:
        return x1, y1, x2, y2
    else:
        return None

def visualize_line_clipping(x_min, y_min, x_max, y_max, lines):

    plt.figure(figsize=(8, 6))
    plt.title("Cohen-Sutherland Line Clipping")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")

    # Plot the clipping window
    plt.plot([x_min, x_max, x_max, x_min, x_min], [y_min, y_min, y_max, y_max, y_min], 'r-', label='Clipping Window')

    for x1, y1, x2, y2 in lines:
        # Plot the original line
        plt.plot([x1, x2], [y1, y2], 'b--')
        # Clip the line
        result = cohen_sutherland_line_clip(x_min, y_min, x_max, y_max, x1, y1, x2, y2)
        if result:
            x1_clip, y1_clip, x2_clip, y2_clip = result
            # Plot the clipped line
            plt.plot([x1_clip, x2_clip], [y1_clip, y2_clip], 'g-')
        else:
            print(f"Line ({x1}, {y1}) to ({x2}, {y2}) is completely outside the clipping window.")

    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # Clipping window coordinates
    x_min, y_min = 50, 50
    x_max, y_max = 200, 200

    # Generate 5 random lines
    num_lines = 5
    lines = []
    for _ in range(num_lines):
        x1 = random.randint(0, 250)  # Adjust range as needed
        y1 = random.randint(0, 250)
        x2 = random.randint(0, 250)
        y2 = random.randint(0, 250)
        lines.append((x1, y1, x2, y2))

    visualize_line_clipping(x_min, y_min, x_max, y_max, lines)
