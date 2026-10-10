import math
import random

import pytest

from bresenham_circle import bresenham_circle
from bresenham_line import bresenham_line
from cohen_sutherland import cohen_sutherland_line_clip
from dda_line import dda_algorithm
from liang_barsky import liang_barsky_line_clip
from midpoint_circle import midpoint_circle_points
from midpoint_ellipse import midpoint_ellipse
from sutherland_hodgman import clip_polygon


def is_connected(points):
    """Each pixel touches the next one (8-connected)."""
    return all(max(abs(x2 - x1), abs(y2 - y1)) == 1 for (x1, y1), (x2, y2) in zip(points, points[1:]))


# ---------- Lines ----------

@pytest.mark.parametrize("line", [(0, 0, 10, 4), (0, 0, 4, 10), (10, 4, 0, 0), (2, 8, 9, 1), (0, 0, 7, 0), (3, 3, 3, 9)])
def test_bresenham_line_runs_from_end_to_end_without_gaps(line):
    x1, y1, x2, y2 = line
    points = bresenham_line(x1, y1, x2, y2)
    assert points[0] == (x1, y1)
    assert points[-1] == (x2, y2)
    assert len(points) == max(abs(x2 - x1), abs(y2 - y1)) + 1
    assert is_connected(points)


def test_dda_matches_the_ideal_line():
    xs, ys = dda_algorithm(0, 0, 8, 4)
    assert list(zip(xs, ys))[0] == (0, 0) and list(zip(xs, ys))[-1] == (8, 4)
    for x, y in zip(xs, ys):
        assert abs(y - x / 2) <= 0.5


def test_dda_handles_a_single_point():
    assert dda_algorithm(5, 5, 5, 5) == ([5], [5])  # used to divide by zero


# ---------- Circles and ellipses ----------

@pytest.mark.parametrize("algorithm", [lambda r: bresenham_circle(0, 0, r), lambda r: midpoint_circle_points(r, 0, 0)])
@pytest.mark.parametrize("r", [1, 5, 20, 57, 150])
def test_circle_points_lie_on_the_circle(algorithm, r):
    points = algorithm(r)
    for x, y in points:
        assert abs(math.hypot(x, y) - r) <= 0.5 + 1e-9  # every pixel is the nearest one to the circle
    assert (r, 0) in points and (0, r) in points and (-r, 0) in points and (0, -r) in points


def test_circle_is_centred_where_asked():
    points = midpoint_circle_points(10, 30, -20)
    xs, ys = zip(*points)
    assert (min(xs) + max(xs)) / 2 == 30
    assert (min(ys) + max(ys)) / 2 == -20


@pytest.mark.parametrize("rx, ry", [(10, 5), (5, 10), (20, 20), (30, 7)])
def test_ellipse_points_lie_on_the_ellipse(rx, ry):
    points = midpoint_ellipse(0, 0, rx, ry)
    for x, y in points:
        # distance from the ellipse, measured along the ray from the centre, is under a pixel
        t = math.atan2(y / ry, x / rx)
        ex, ey = rx * math.cos(t), ry * math.sin(t)
        assert math.hypot(x - ex, y - ey) < 1.5
    assert (rx, 0) in points and (0, ry) in points


# ---------- Clipping ----------

WINDOW = (50, 50, 200, 200)


def test_line_fully_inside_is_kept():
    assert cohen_sutherland_line_clip(*WINDOW, 60, 60, 150, 100) == (60, 60, 150, 100)
    assert liang_barsky_line_clip(*WINDOW, 60, 60, 150, 100) == (60, 60, 150, 100)


def test_line_fully_outside_is_rejected():
    assert cohen_sutherland_line_clip(*WINDOW, 0, 0, 40, 300) is None
    assert liang_barsky_line_clip(*WINDOW, 0, 0, 40, 300) is None


def test_line_crossing_the_window_is_cut_at_the_edges():
    result = liang_barsky_line_clip(*WINDOW, 0, 100, 250, 100)
    assert result == (50, 100, 200, 100)


def test_cohen_sutherland_and_liang_barsky_agree():
    rng = random.Random(3)
    for _ in range(500):
        line = [rng.randint(0, 250) for _ in range(4)]
        a = cohen_sutherland_line_clip(*WINDOW, *line)
        b = liang_barsky_line_clip(*WINDOW, *line)
        if a is None or b is None:
            # Liang-Barsky may keep a single touching point that Cohen-Sutherland drops
            kept = a or b
            assert kept is None or (abs(kept[0] - kept[2]) < 1e-9 and abs(kept[1] - kept[3]) < 1e-9)
            continue
        # The two methods may return the ends in a different order
        ends_a = sorted([(round(a[0], 6), round(a[1], 6)), (round(a[2], 6), round(a[3], 6))])
        ends_b = sorted([(round(b[0], 6), round(b[1], 6)), (round(b[2], 6), round(b[3], 6))])
        assert ends_a == ends_b


def polygon_area(points):
    return abs(sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(points, points[1:] + points[:1]))) / 2


def test_polygon_clipping_keeps_the_overlap():
    square = [(100, 100), (300, 100), (300, 300), (100, 300)]
    clipped = clip_polygon(square, [150, 150, 250, 250])
    assert polygon_area(clipped) == pytest.approx(100 * 100)


def test_polygon_clipping_of_a_triangle_corner():
    triangle = [(0, 0), (200, 0), (0, 200)]
    clipped = clip_polygon(triangle, [0, 0, 100, 100])
    assert polygon_area(clipped) == pytest.approx(100 * 100)  # the triangle covers the whole box


def test_polygon_outside_the_window_disappears():
    assert clip_polygon([(0, 0), (10, 0), (5, 10)], [100, 100, 200, 200]) == []
