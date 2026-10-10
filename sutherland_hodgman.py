import matplotlib.pyplot as plt
import random

def clip_polygon(polygon, clip_window):

    xmin, ymin, xmax, ymax = clip_window
    clipped_polygon = list(polygon)  

    clipping_edges = [
        ("left", (xmin, ymin), (xmin, ymax)),
        ("right", (xmax, ymin), (xmax, ymax)),
        ("bottom", (xmin, ymin), (xmax, ymin)),
        ("top", (xmin, ymax), (xmax, ymax)),
    ]

    for edge_name, edge_start, edge_end in clipping_edges:
        input_list = clipped_polygon
        clipped_polygon = [] 

        if not input_list:
            continue

        for i in range(len(input_list)):
            current_vertex = input_list[i]
            prev_vertex = input_list[(i - 1) % len(input_list)]  

            inside_current = _is_inside(current_vertex, edge_name, xmin, ymin, xmax, ymax)
            inside_prev = _is_inside(prev_vertex, edge_name, xmin, ymin, xmax, ymax)

            if inside_current:
                if not inside_prev:
                    intersection = _get_intersection(prev_vertex, current_vertex, edge_start, edge_end)
                    if intersection is not None:
                        clipped_polygon.append(intersection)
                clipped_polygon.append(current_vertex)
            elif inside_prev:
                intersection = _get_intersection(prev_vertex, current_vertex, edge_start, edge_end)
                if intersection is not None:
                    clipped_polygon.append(intersection)

    return clipped_polygon


def _is_inside(vertex, edge_name, xmin, ymin, xmax, ymax):

    x, y = vertex
    if edge_name == "left":
        return x >= xmin
    elif edge_name == "right":
        return x <= xmax
    elif edge_name == "bottom":
        return y >= ymin
    elif edge_name == "top":
        return y <= ymax
    return False  # Should not reach here


def _get_intersection(p1, p2, edge_start, edge_end):

    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = edge_start
    x4, y4 = edge_end

    # Intersection = p1 + u * (p2 - p1), where
    # u = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
    denominator = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    if denominator == 0:
        return None  

    u = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denominator
    x = x1 + u * (x2 - x1)
    y = y1 + u * (y2 - y1)
    return x, y


def visualize_polygon_clipping(polygon, clip_window, clipped_polygon):

    xmin, ymin, xmax, ymax = clip_window

    # Create the plot
    plt.figure(figsize=(8, 6))
    plt.title("Sutherland-Hodgman Polygon Clipping")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")

    # Plot the original polygon
    x_original, y_original = zip(*polygon)
    x_original = list(x_original) + [x_original[0]]  # Close the polygon
    y_original = list(y_original) + [y_original[0]]
    plt.plot(x_original, y_original, 'b-')  # Removed label

    # Plot the clipping window
    x_clip = [xmin, xmax, xmax, xmin, xmin]
    y_clip = [ymin, ymin, ymax, ymax, ymin]
    plt.plot(x_clip, y_clip, 'r-', label='Clipping Window')

    # Plot the clipped polygon
    if clipped_polygon:
        x_clipped, y_clipped = zip(*clipped_polygon)
        x_clipped = list(x_clipped) + [x_clipped[0]]  # Close the polygon
        y_clipped = list(y_clipped) + [y_clipped[0]]
        plt.plot(x_clipped, y_clipped, 'g-')  # Removed label
    else:
        print("Polygon is completely outside the clipping window.")

    # Add legend and grid
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # Define the clipping window
    clip_window = [150, 150, 250, 250]

    # Generate a random polygon
    num_vertices = random.randint(3, 8)  # Random number of vertices between 3 and 8
    polygon = []
    for _ in range(num_vertices):
        x = random.randint(0, 300)  # Adjust range as needed
        y = random.randint(0, 300)  # Adjust range as needed
        polygon.append((x, y))

    # Clip the polygon
    clipped_polygon = clip_polygon(polygon, clip_window)

    # Visualize the result
    visualize_polygon_clipping(polygon, clip_window, clipped_polygon)
