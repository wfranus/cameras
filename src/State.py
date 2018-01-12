import random, sys, copy
from src.Camera import Camera


class State:
    def __init__(self, problem, cameras=None):
        self.problem = problem
        self.cameras = []
        self.cameras = cameras if cameras is not None else self.generateCameras()
        self.energy = sys.maxsize
        self.coverage_energy = None
        self.camera_cost = None
        self.redundancy_cost = None

    def getRandomFreePointFromRoom(self):
        free_points = self.getFreePoints()
        if not free_points:
            error = "Exception in State.getRandomFreePointFromRoom: no points left!"
            raise RuntimeError(error)
        else:
            return random.choice(free_points)

    def getFreePoints(self):
        def isCameraPos(cls, pos):
            for c in cls.cameras:
                if c.x == pos[0] and c.y == pos[1]:
                    return True
            return False

        return list(filter(lambda p: not isCameraPos(self, p), self.problem.inside_points))

    def generateCameras(self):
        cameras = []
        for _ in range(self.problem.min_number_of_cams):
            cameras.append(Camera(self.problem, self.getRandomFreePointFromRoom()))

        return cameras

    def generateNeighbour(self, camera_move_method):
        # deep copy cameras
        cameras = [copy.copy(c) for c in self.cameras]

        transformation = self.randomlyChooseTransformationMethod(cameras)

        # perform transformation
        if transformation == 'insert':
            new_camera = Camera(self.problem, self.getRandomFreePointFromRoom())
            cameras.append(new_camera)
        elif transformation == 'remove':
            cameras.remove(random.choice(self.cameras))
        elif transformation == 'move':
            to_modify = random.choice(self.cameras)
            if camera_move_method == 'local':
                to_modify.move()
            elif camera_move_method == 'random':
                to_modify.move(self.getRandomFreePointFromRoom())
            else:
                raise RuntimeError("Wrong move camera method!")
        else:
            raise RuntimeError("Wrong transformation method!")

        return State(self.problem, cameras)

    def randomlyChooseTransformationMethod(self, cameras):
        free_points = self.getFreePoints()
        choices = set()

        if len(cameras) <= 1:
            choices.add('insert')
        else:
            choices.add('remove')
            if len(free_points) > 0:
                choices.update({'insert', 'move'})
        return random.choice(tuple(choices))
