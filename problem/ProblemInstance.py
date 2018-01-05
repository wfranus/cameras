from matplotlib import path
from shapely.geometry import LineString
import numpy as np
import math


class ProblemInstance:
    def __init__(self, config_validator):
        self.config_validator = config_validator
        try:
            self.camera_side = config_validator.getIntegerParameter('camera_side', 1)
            self.r_min = config_validator.getIntegerParameter('r_min', 1)
            self.alpha = config_validator.getDoubleParameter('alpha', 1.0)
            self.beta = config_validator.getDoubleParameter('beta', 1.0)
            self.room_path, self.room_points, self.walls = \
                ProblemInstance.loadRoomFromConfig(config_validator.getParameter('room'))
            self.min_number_of_cams = self.calculateMinNumberOfCams()
            self.bbox_points = self.calculateBoundingBox()
            self.inside_points = self.calculateInsidePoints(self.bbox_points)
        except KeyError as e:
            print("Error: Option {} is missing in config file".format(e))

    @staticmethod
    def loadRoomFromConfig(room):
        # read room vertices from config
        points = []
        for vertex in room:
            x = vertex['x']
            y = vertex['y']
            point = (x, y)
            points.append(point)

        walls = LineString(points)
        room_path = path.Path(points, closed=True)
        return room_path, points, walls

    def calculateInsidePoints(self, bbox):
        inside_points = []
        for point in bbox:
            if self.room_path.contains_point(point, radius=0.1):
                inside_points.append((point[0], point[1]))

        return inside_points

    def calculateBoundingBox(self):
        # get bounding box of room
        bbox = path.get_paths_extents([self.room_path])
        (width, height) = bbox.size

        # get all points inside bbox
        x, y = np.meshgrid(np.arange(width+1), np.arange(height+1))
        x, y = x.flatten(), y.flatten()
        return np.vstack((x, y)).T

    def calculateMinNumberOfCams(self):
        camera_area = self.camera_side * self.camera_side
        polygon_area = ProblemInstance.polygonArea(self.room_points)
        return math.ceil(polygon_area / camera_area)

    @staticmethod
    def polygonArea(room_points):
        n = len(room_points)  # of corners
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += room_points[i][0] * room_points[j][1]
            area -= room_points[j][0] * room_points[i][1]
        area = abs(area) / 2.0
        return area

