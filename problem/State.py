import random
import copy
from problem.Camera import Camera


class State:
    def __init__(self, problem, cameras=None):
        self.problem = problem
        self.cameras = []
        self.cameras = cameras if cameras is not None else self.generateCameras()

    def getRandomFreePointFromRoom(self):
        def isCameraPos(cls, pos):
            for c in cls.cameras:
                if c.x == pos[0] and c.y == pos[1]:
                    return True
            return False

        free_points = list(filter(lambda p: not isCameraPos(self, p), self.problem.inside_points))

        if not free_points:
            error = "Exception in State.getRandomFreePointFromRoom: no points left!"
            raise RuntimeError(error)
        else:
            return random.choice(free_points)

    def generateCameras(self):
        cameras = []
        for _ in range(self.problem.min_number_of_cams):
            cameras.append(Camera(self.problem, self.getRandomFreePointFromRoom()))

        return cameras

    def generateNeighbour(self, camera_move_method):
        # deep copy cameras
        cameras = [copy.copy(c) for c in self.cameras]

        # randomly choose transformation
        if len(cameras) == 0:
            transformation = 'insert'
        elif len(cameras) == 1:
            transformation = random.choice(['insert', 'move'])
        else:
            transformation = random.choice(['insert', 'remove', 'move'])

        # perform transformation
        if transformation == 'insert':
            newCamera = Camera(self.problem, self.getRandomFreePointFromRoom())
            cameras.append(newCamera)
        elif transformation == 'remove':
            cameras.remove(random.choice(self.cameras))
        else:
            toModify = random.choice(self.cameras)
            if camera_move_method == 'local':
                toModify.move()
            elif camera_move_method == 'random':
                toModify.move(self.getRandomFreePointFromRoom())
            else:
                print("Wrong move camera method!")
                raise RuntimeError

        # return new state
        return State(self.problem, cameras)
