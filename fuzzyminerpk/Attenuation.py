from abc import ABC, abstractmethod
import numpy as np


class Attenuation(ABC):
    def __init__(self, buf_size=10, attenuation_factors=None):
        self.buf_size = buf_size
        self.attenuation_factors = attenuation_factors

    def attenuate(self, value, distance):
        return value * self.get_attenuation_factor(distance)

    def get_attenuation_factor(self, distance):
        if distance < self.buf_size:
            if self.attenuation_factors is None:
                self.generate_buffer()
            return self.attenuation_factors[distance]
        else:
            return self.create_attenuation_factor(distance)

    def generate_buffer(self):
        self.attenuation_factors = []
        for i in range(self.buf_size):
            self.attenuation_factors.append(self.create_attenuation_factor(i))

    @abstractmethod
    def create_attenuation_factor(self, distance):
        pass

    @abstractmethod
    def get_name(self):
        pass

    def __str__(self):
        return "Buffer Size: " + str(self.buf_size) + " Attenuation Factor: " + self.attenuation_factors


class LinearAttenuation(Attenuation):

    def __init__(self, buffer_size, num_of_echelons):
        super().__init__(buffer_size)
        self.echelons = num_of_echelons

    def create_attenuation_factor(self, distance):
        if distance == 1:
            return 1.0
        else:
            return float(self.echelons - distance + 1) / float(self.echelons)

    def get_name(self):
        return "Linear Attenuation"

    def __str__(self):
        return " Echelons Value: " + str(self.echelons)


class NRootAttenuation(Attenuation):

    # Keep in mind the order in java code for buffer_size and num_of_echelon is reverse
    def __init__(self, buffer_size, num_of_echelons):
        super().__init__(buffer_size)
        self.echelons = num_of_echelons

    def create_attenuation_factor(self, distance):
        if distance == 1:
            return 1.0
        else:
            return 1.0 / pow(self.echelons, distance - 1)

    def get_name(self):
        if self.echelons == 2:
            return "Square root"
        elif self.echelons == 3:
            return "Cubic root"
        elif self.echelons == 4:
            return "Quadratic root"
        else:
            return str(self.echelons) + "th root"

    def __str__(self):
        return " Echelons Value: " + str(self.echelons)
