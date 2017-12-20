from matplotlib import path

import numpy as np
from problem.ConfigValidator import ConfigValidator

class ProblemInstance:
    def __init__(self, config):
        try:
            self.loadAndValidateConfig(config)
        except KeyError as e:
            print("Exception. Option {} is missing in config file".format(e))

    def loadAndValidateConfig(self, config):
        self.camera_range = ConfigValidator.validateIntegerParameter(config, 'camera_range', 1)
        self.r_min = ConfigValidator.validateIntegerParameter(config, 'r_min', 1)
        self.alpha = ConfigValidator.validateDoubleParameter(config, 'alpha', 1.0)
        self.beta = ConfigValidator.validateDoubleParameter(config, 'beta', 1.0)
        self.loadRoomFromConfig(config['room'])
        self.minNumberOfCams = self.calculateMinNumberOfCams()
        self.insidePoints = self.calculateInsidePoints()


    def loadRoomFromConfig(self, room):
        # read room vertices from config
        points = []
        for vertex in room:
            x = vertex['x']
            y = vertex['y']
            point = (x,y)
            points.append(point)
        self.room = path.Path(points, closed=True)
        self.roomPoints = points


    def calculateInsidePoints(self):
        # get bounding box of room
        bbox = path.get_paths_extents([self.room])
        #print('BBox', bbox)
        (width, height) = bbox.size

        # get all points inside bbox
        x, y = np.meshgrid(np.arange(width+1), np.arange(height+1))
        x, y = x.flatten(), y.flatten()
        bbox_points = np.vstack((x,y)).T

        in_points_x = []
        in_points_y = []
        insidePoints = []
        for point in bbox_points:
            #print(point, self.room.contains_point(point, radius=-0.1))
            if self.room.contains_point(point, radius=-0.1):
                insidePoints.append((point[0], point[1]))
                in_points_x.append(point[0])
                in_points_y.append(point[1])

        return insidePoints

    def calculateMinNumberOfCams(self):
        return self.polygonArea(self.roomPoints) / self.camera_range

    def getInitialState(self):
        #TODO create list of tuples - cameras coords
        return []

    def polygonArea(self, room_points):
        n = len(room_points) # of corners
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += room_points[i][0] * room_points[j][1]
            area -= room_points[j][0] * room_points[i][1]
        area = abs(area) / 2.0
        return area
