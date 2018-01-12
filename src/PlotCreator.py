from matplotlib import path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math


class PlotCreator:

    def __init__(self):
        pass

    @staticmethod
    def calculatePointSize(inches, bbox_points):
        inch = 96  # 1inch ~= 96 pixels
        point_size = inch * inches / math.sqrt(len(bbox_points))
        return point_size

    @staticmethod
    def createStatePlot(file_name, state, room_only=False):
        inches = 10
        point_size = PlotCreator.calculatePointSize(inches, state.problem.bbox_points)

        fig = plt.figure(figsize=(inches, inches))
        ax = fig.add_subplot(111)
        room_patch = patches.PathPatch(state.problem.room_path,
                                       facecolor='lightblue',
                                       lw=1, zorder=1)
        ax.add_patch(room_patch)

        # draw points inside room
        in_points_x = []
        in_points_y = []
        for point in state.problem.inside_points:
            in_points_x.append(point[0])
            in_points_y.append(point[1])
        inside_plot_point = plt.scatter(in_points_x, in_points_y,
                                        color="purple", s=point_size, zorder=2)

        # draw point covered by cameras
        if not room_only:
            cam_center_x = []
            cam_center_y = []
            for c in state.cameras:
                cam_center_x.append(c.x)
                cam_center_y.append(c.y)

                cam_covered_points_x = []
                cam_covered_points_y = []
                for p in c.covered_points:
                    cam_covered_points_x.append(p[0])
                    cam_covered_points_y.append(p[1])
                cam_plot_covered_point = plt.scatter(cam_covered_points_x, cam_covered_points_y,
                                                     color="yellow", s=point_size, zorder=4)

            cam_plot_center_point = plt.scatter(cam_center_x, cam_center_y,
                                                color="red", s=point_size*2, zorder=5)

        # name axis
        plt.ylabel('y')
        plt.xlabel('x')

        # create legend
        if room_only:
            plt.legend([room_patch, (room_patch, inside_plot_point)],
                       ["room", "point inside room"])
        else:
            plt.legend([inside_plot_point, cam_plot_covered_point, cam_plot_center_point],
                       ["not covered point", "covered point", "camera position"])

        fig.savefig(file_name + '.png', dpi=180, bbox_inches='tight')
        plt.close()

    @staticmethod
    def createCostPlot(file_name, costs):
        fig = plt.figure(figsize=(10, 10))

        ymin = min(costs)
        ymax = max(costs)
        plt.ylim(ymin, ymax)

        plt.plot(range(len(costs)), costs)
        plt.ylabel('cost')
        plt.xlabel('iteration')

        fig.savefig(file_name + '.png', dpi=90)
        plt.close()

