import random
import copy
from problem.Camera import Camera


class State:
    def __init__(self, problem, cameras=None):
        self.problem = problem
        self.cameras = []
        self.cameras = cameras if cameras else self.generateCameras()

    def getRandomFreePointFromRoom(self):
        def isCameraPos(pos):
            for c in self.cameras:
                if c.x == pos[0] and c.y == pos[1]:
                    return True
            return False

        return random.choice([p for p in self.problem.insidePoints if not isCameraPos(p)])

    def generateCameras(self):
        cameras = []
        for _ in range(self.problem.minNumberOfCams):
            cameras.append(Camera(self.problem, self.getRandomFreePointFromRoom()))

        return cameras

    def generateNeighbour(self, cameraMoveMethod):
        # deep copy cameras
        cameras = [copy.copy(c) for c in self.cameras]

        # randomly choose transformation
        if len(cameras) == 1:
            transformation = random.choice(['insert', 'move'])
        else:
            transformation = random.choice(['insert', 'remove', 'move'])

        # perform transformation
        if transformation == 'insert':
            newCamera = Camera(self.problem, self.getRandomFreePointFromRoom())
            self.cameras.append(newCamera)
        elif transformation == 'remove':
            cameras.remove(random.choice(self.cameras))
        else:
            toModify = random.choice(self.cameras)
            if cameraMoveMethod == 'local':
                toModify.move()
            elif cameraMoveMethod == 'random':
                toModify.move(self.getRandomFreePointFromRoom())
            else:
                print("Wrong move camera method!")
                raise RuntimeError

        # return new state
        return State(self.problem, cameras)
