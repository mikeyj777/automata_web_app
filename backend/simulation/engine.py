# backend/simulation/engine.py

import time
import threading
from models.agent import Agent
import numpy as np
import random

class SimulationEngine:
    def __init__(self, bounds=(100, 100), params=None):
        self.bounds = bounds
        self.agents = []
        self.nodes = [(20, 20), (80, 80)]  # Example nodes
        self.poles = [(20, 80), (80, 20)]  # Example poles
        self.running = False
        self.params = params or {
            'neighbor_distance': 10.0,
            'alignment_weight': 0.05,
            'cohesion_weight': 0.01,
            'separation_weight': 0.1,
            'max_speed': 2.0,
            'task_speed': 3.0,
            'task_threshold': 1.0,
            'reproduction_probability': 0.01
        }
        self.lock = threading.Lock()

    def initialize_agents(self, num_agents=50):
        for _ in range(num_agents):
            position = np.random.uniform(0, self.bounds[0], size=2)
            angle = random.uniform(0, 2 * np.pi)
            velocity = np.array([np.cos(angle), np.sin(angle)]) * self.params['max_speed']
            agent = Agent(position, velocity)
            self.agents.append(agent)

    def update(self):
        with self.lock:
            new_agents = []
            for agent in self.agents:
                agent.apply_flocking(self.agents, self.params)
                agent.update_position(self.bounds)
                new_agent = agent.reproduce(self.agents, self.params)
                if new_agent:
                    new_agents.append(new_agent)
                agent.assign_task(self.nodes, self.poles, self.params)
                agent.perform_task(self.params)
            self.agents.extend(new_agents)

    def get_state(self):
        with self.lock:
            return [
                {
                    'id': agent.id,
                    'position': agent.position.tolist(),
                    'velocity': agent.velocity.tolist(),
                    'state': agent.state,
                    'task': agent.task
                }
                for agent in self.agents
            ]

    def run(self, update_interval=0.1):
        self.running = True
        while self.running:
            self.update()
            time.sleep(update_interval)

    def stop(self):
        self.running = False
