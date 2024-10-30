import json

class Signal_information(object):
    def __init__(self, signal_power: float, path: list[str]):
        
        self._signal_power = signal_power
        self._noise_power = 0.0
        self._latency = 0.0
        self._path = path

    @property
    def get_signal_power(self) -> float:
        return self._signal_power

    def update_signal_power(self, increment: float):
        self._signal_power += increment

    @property
    def get_noise_power(self) -> float:
        return self._noise_power

    @noise_power.setter
    def set_noise_power(self, noise_power: float):
        self._noise_power = noise_power

    def update_noise_power(self, increment: float):
        self._noise_power += increment

    @property
    def get_latency(self):
        return self._latency

    @latency.setter
    def set_latency(self, latency: float):
        self._latency = latency

    def update_latency(self, increment: float):
        

    @property
    def get_path(self) -> list[str]:
        return self._path

    @path.setter
    def set_path(self, path: list[str]):
        self._path = path

    def update_path(self, increment: float):
        if self._path:
            self._path.pop(0)


class Node(object):
    def __init__(self):
        pass

    @property
    def label(self):
        pass

    @property
    def position(self):
        pass

    @property
    def connected_nodes(self):
        pass

    @property
    def successive(self):
        pass

    @successive.setter
    def successive(self):
        pass

    def propagate(self):
        pass


class Line(object):
    def __init__(self):
        pass

    @property
    def label(self):
        pass

    @property
    def length(self):
        pass

    @property
    def successive(self):
        pass

    @successive.setter
    def successive(self):
        pass

    def latency_generation(self):
        pass

    def noise_generation(self):
        pass

    def propagate(self):
        pass


class Network(object):
    def __init__(self):
        pass

    @property
    def nodes(self):
        pass

    @property
    def lines(self):
        pass

    def draw(self):
        pass

    # find_paths: given two node labels, returns all paths that connect the 2 nodes
    # as a list of node labels. Admissible path only if cross any node at most once
    def find_paths(self, label1, label2):
        pass

    # connect function set the successive attributes of all NEs as dicts
    # each node must have dict of lines and viceversa
    def connect(self):
        pass

    # propagate signal_information through path specified in it
    # and returns the modified spectral information
    def propagate(self, signal_information):
        pass
