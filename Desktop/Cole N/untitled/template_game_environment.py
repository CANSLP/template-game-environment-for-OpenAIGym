import time
import random

"""
Classic cart-pole system implemented by Rich Sutton et al.
Copied from http://incompleteideas.net/sutton/book/code/pole.c
permalink: https://perma.cc/C9ZM-652R
"""

import math
import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np

class GameEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second' : 50
    }

    def __init__(self):
        #game variables

        high = np.array([0,0,0,0])


        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(-high, high)

        self.seed()
        self.viewer = None
        self.state = None

        self.steps_beyond_done = None

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        state = self.state
        #game mechanics

        done = False

        if not done:
            reward = 1.0
        elif self.steps_beyond_done is None:
            # Game Over?
            self.steps_beyond_done = 0
            reward = 1.0
        else:
            if self.steps_beyond_done == 0:
                logger.warn("You are calling 'step()' even though this environment has already returned done = True. You should always call 'reset()' once you receive 'done = True' -- any further steps are undefined behavior.")
            self.steps_beyond_done += 1
            reward = 0.0

        return np.array(self.state), reward, done, {}

    def reset(self):
        self.state = self.np_random.uniform(low=-0.05, high=0.05, size=(4,))
        self.steps_beyond_done = None
        return np.array(self.state)

    def render(self, mode='human'):
        screen_width = 1000
        screen_height = 1000


        #rendering game variables

        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(screen_width, screen_height)

            #render game objects

            #self.Object = rendering.Function(?,?,...)
            #self.viewer.add_geom(self.Object)

            #self.Object.set_color(r,g,b)

            #rendering.
            # FilledPolygon([(,),(,),...])
            #Transform()
            #make_circle()
            #Line(,)

            #example orange background
            self.back = rendering.FilledPolygon([(0,0),(screen_width,0),(screen_width,screen_height),(0,screen_height)])
            self.back.set_color(1,0.5,0)
            self.viewer.add_geom(self.back)



        if self.state is None: return None

        #set initial game variable values

        return self.viewer.render(return_rgb_array = mode=='rgb_array')

    def close(self):
        if self.viewer: self.viewer.close()


game = GameEnv();
game.reset()
for tick in range(100):
    game.step(random.randint(0,1))
    game.render()
    time.sleep(1/50)

game.close()