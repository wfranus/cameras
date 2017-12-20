from matplotlib import path

import numpy as np

class ProblemInstance:
    def __init__(self, config):
        try:
            self.alpha = config['alpha']
            self.beta = config['beta']
            self.rMin = config['r_min']
            self.room = self.loadRoomFromConfig(config['room'])
            self.minNumberOfCams = self.calculateMinNumberOfCams()
            self.insidePoints = self.calculateInsidePoints()
        except KeyError as e:
            print("Exception. Option {} is missing in config file".format(e))

    def loadRoomFromConfig(self, room):
        # read room vertices from config
        points = []
        for vertex in room:
            x = vertex['x']
            y = vertex['y']
            point = (x,y)
            points.append(point)
        return path.Path(points, closed=True)

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
        #TODO
        return 1