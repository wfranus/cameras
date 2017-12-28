import random
from matplotlib import path
import numpy as np
import matplotlib.patches as patches
import matplotlib.pyplot as plt


class Camera:
    def __init__(self, problem, pos):
        self.problem = problem
        self.x = float(pos[0])
        self.y = float(pos[1])
        self.covered_points = self.getCoveredPoints()

    def __eq__(self, other):
        return self.problem == other.problem \
               and self.x == other.x and self.y == other.y

    def move(self, new_pos=None):
        if new_pos:
            self.x = float(new_pos[0])
            self.y = float(new_pos[1])
        else:
            self.x += random.choice([-1, 0, 1])
            self.y += random.choice([-1, 0, 1])

    def getCameraRect(self):
        rect_side = self.problem.camera_side
        diff = rect_side / 2
        rect_vertices = [
            (self.x - diff, self.y - diff),
            (self.x - diff, self.y + diff),
            (self.x + diff, self.y + diff),
            (self.x + diff, self.y - diff),
            (self.x - diff, self.y - diff),  # doubled first vertex
        ]
        return path.Path(rect_vertices, closed=True)

    def getCoveredPoints(self):
        covered_points = []

        # create camera range rectangle
        rect = self.getCameraRect()

        # get all points inside both camera range and room
        for point in self.problem.inside_points:
            np_point = np.array([point[0], point[1]])
            if rect.contains_point(np_point, radius=-0.1):
                covered_points.append(point)

        #print("Camera ({}, {}) points: {}".format(self.x, self.y, covered_points))

        # in_points_x = []
        # in_points_y = []
        # for point in covered_points:
        #     in_points_x.append(point[0])
        #     in_points_y.append(point[1])
        #
        # fig = plt.figure()
        # ax = fig.add_subplot(111)
        # patch = patches.PathPatch(self.problem.room_path, facecolor='orange', lw=1, zorder=1)
        # ax.add_patch(patch)
        # # auto adjust plot axis range
        # ax.set_xlim(-1, 10)
        # ax.set_ylim(-1, 10)
        # plt.scatter(in_points_x, in_points_y, s=10, zorder=2)
        # plt.show()

        return covered_points
