from matplotlib import path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
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
        print('BBox', bbox)
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
                self.insidePoints.append((point[0], point[1]))
                in_points_x.append(point[0])
                in_points_y.append(point[1])

        #TODO: move this to visualizer class
        fig = plt.figure()
        ax = fig.add_subplot(111)
        patch = patches.PathPatch(self.room, facecolor='orange', lw=1, zorder=1)
        ax.add_patch(patch)
        # auto adjust plot axis range
        ax.set_xlim(bbox.p0[0] - 1, bbox.p1[0] + 1)
        ax.set_ylim(bbox.p0[1] - 1, bbox.p1[1] + 1)
        plt.scatter(in_points_x, in_points_y, s=10, zorder=2)
        plt.show()
        ###########

        return insidePoints

    def calculateMinNumberOfCams(self):
        #TODO
        return 1