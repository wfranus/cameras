import random
import copy


class State:
    def __init__(self, problem, cameras=None):
        self.problem = problem
        self.cameras = cameras if cameras else self.generate_cameras()
        self.num_unobserved = None

    def generate_cameras(self):

        # generated cameras
        cameras = []

        # return generated cameras
        return cameras

    def generate_neighbour(self):
        #TODO modify current state
        # deep copy cameras
        cameras = [copy.copy(c) for c in self.cameras]

        # modify state

        # return new state
        return State(self.problem, cameras)
