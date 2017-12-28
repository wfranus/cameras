from matplotlib import path
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class PlotCreator:

    def __init__(self):
        pass

    @staticmethod
    def createStatePlot(file_name, state, room_only=False):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        room_patch = patches.PathPatch(state.problem.room_path,
                                       facecolor='lightblue',
                                       lw=1, zorder=1)
        ax.add_patch(room_patch)

        # # adjust plot axis range
        # room_bbox = path.get_paths_extents([room_path])
        # ax.set_xlim(room_bbox.p0[0] - 1, room_bbox.p1[0] + 1)
        # ax.set_ylim(room_bbox.p0[1] - 1, room_bbox.p1[1] + 1)

        # draw points inside room
        in_points_x = []
        in_points_y = []
        for point in state.problem.inside_points:
            in_points_x.append(point[0])
            in_points_y.append(point[1])
        inside_plot_point = plt.scatter(in_points_x, in_points_y,
                                        color="purple", s=10, zorder=2)

        # draw point covered by cameras
        if not room_only:
            for c in state.cameras:
                cam_points_x = []
                cam_points_y = []
                for p in c.covered_points:
                    cam_points_x.append(p[0])
                    cam_points_y.append(p[1])
                cam_patch = patches.PathPatch(c.getCameraRect(),
                                              fill=False, color="blue",
                                              lw=1, zorder=1)
                ax.add_patch(cam_patch)
                cam_plot_point = plt.scatter(cam_points_x, cam_points_y,
                                             color="yellow", s=10, zorder=3)

        # name axis
        plt.ylabel('y')
        plt.xlabel('x')

        # create legend
        if room_only:
            plt.legend([room_patch, (room_patch, inside_plot_point)],
                       ["room", "point inside room"])
        else:
            plt.legend([inside_plot_point, (inside_plot_point, cam_plot_point)],
                       ["not covered point", "covered point"])

        fig.savefig(file_name + '.png', dpi=180, bbox_inches='tight')

    @staticmethod
    def createCostPlot(file_name, costs):
        fig = plt.figure(figsize=(10, 10))

        plt.plot(range(len(costs)), costs)
        plt.ylabel('cost')
        plt.xlabel('iteration')

        fig.savefig(file_name + '.png', dpi=90)
