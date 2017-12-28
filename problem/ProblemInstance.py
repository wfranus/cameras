from matplotlib import path

import numpy as np

class ProblemInstance:
    def __init__(self, config_validator):
        self.config_validator = config_validator
        try:
            self.camera_range = config_validator.getIntegerParameter('camera_range', 1)
            self.r_min = config_validator.getIntegerParameter('r_min', 1)
            self.alpha = config_validator.getDoubleParameter('alpha', 1.0)
            self.beta = config_validator.getDoubleParameter('beta', 1.0)
            self.room_path, self.room_points = self.loadRoomFromConfig(config_validator.getParameter('room'))
            self.min_number_of_cams = self.calculateMinNumberOfCams()
            self.inside_points = self.calculateInsidePoints()
        except KeyError as e:
            print("Error: Option {} is missing in config file".format(e))

    def loadRoomFromConfig(self, room):
        # read room vertices from config
        points = []
        for vertex in room:
            x = vertex['x']
            y = vertex['y']
            point = (x,y)
            points.append(point)
        room_path = path.Path(points, closed=True)
        return room_path, points


    def calculateInsidePoints(self):
        # get bounding box of room
        bbox = path.get_paths_extents([self.room_path])
        (width, height) = bbox.size

        # get all points inside bbox
        x, y = np.meshgrid(np.arange(width+1), np.arange(height+1))
        x, y = x.flatten(), y.flatten()
        bbox_points = np.vstack((x,y)).T

        inside_points = []
        for point in bbox_points:
            if self.room_path.contains_point(point, radius=-0.1):
                inside_points.append((point[0], point[1]))

        return inside_points

    def calculateMinNumberOfCams(self):
        #TODO: czy camera_range to pole powierzchni czy bok kwadratu?
        # jesli to drugie to trzeba podniesc do potegi 2
        camera_area = self.camera_range * self.camera_range
        return self.polygonArea(self.room_points) / camera_area

    def polygonArea(self, room_points):
        n = len(room_points) # of corners
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += room_points[i][0] * room_points[j][1]
            area -= room_points[j][0] * room_points[i][1]
        area = abs(area) / 2.0
        return area
