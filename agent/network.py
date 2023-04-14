import numpy as np
import math


class Network():
    def __init__(self):
        self.weights: list[list[list[float]]] = []
        self.biases: list[list[float]]
        self.activation_values: list[float]

    def compute_actions(self, inputs: list[float]):
        for w, b in zip(self.weights, self.biases):
            inputs = self.sigmoid(np.add(np.dot(w, inputs), b))

        self.activation_values = inputs

    def sigmoid(self, values: np.ndarray) -> list[float]:
        return list(map(lambda val: 1.0 / (1.0 + (math.e ** (-val))), values))
