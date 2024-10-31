import json
import math
import pandas as pd
import matplotlib.pyplot as plt


class signal_information(object):
    def __init__(self, signal_power: float, path: list[str]):
        self._signal_power = signal_power
        self._noise_power = 0.0
        self._latency = 0.0
        self._path = path

    def get_signal_power(self) -> float:
        return self._signal_power

    def update_signal_power(self, increment: float):
        self._signal_power += increment

    def get_noise_power(self) -> float:
        return self._noise_power

    def set_noise_power(self, noise_power: float):
        self._noise_power = noise_power

    def update_noise_power(self, increment: float):
        self._noise_power += increment

    def get_latency(self):
        return self._latency

    def set_latency(self, latency: float):
        self._latency = latency

    def update_latency(self, increment: float):
        self._latency += increment  # Fixed typo here

    def get_path(self) -> list[str]:
        return self._path

    def set_path(self, path: list[str]):
        self._path = path

    def update_path(self):
        if self._path:
            self._path.pop(0)


class Node(object):
    def __init__(self, data: dict):
        self.label = data.get('label', '')
        self.position = data.get('position', (0.0, 0.0))
        self.connected_nodes = data.get('connected_nodes', [])
        self.successive = {}

    def get_label(self) -> str:
        return self.label

    def get_position(self) -> tuple:
        return self.position

    def get_connected_nodes(self) -> list[str]:
        return self.connected_nodes

    def get_successive(self) -> dict:
        return self.successive

    def set_successive(self, successive: dict):
        self.successive = successive

    def propagate(self, signal: 'signal_information'):
        if signal.get_path() and signal.get_path()[0] == self.label:
            signal.update_path()
            if signal.get_path():
                next_node_label = signal.get_path()[0]
                next_node = self.successive.get(next_node_label)
                if next_node:
                    next_node.propagate(signal)


class Line(object):
    SPEED_OF_LIGHT = 3e8
    FIBER_SPEED = SPEED_OF_LIGHT * 2 / 3

    def __init__(self, label: str, length: float):
        self.label = label
        self.length = length
        self.successive = {}

    def get_label(self) -> str:
        return self.label

    def get_length(self) -> float:
        return self.length

    def get_successive(self) -> dict:
        return self.successive

    def set_successive(self, successive: dict):
        self.successive = successive

    def latency_generation(self) -> float:
        return self.length / self.FIBER_SPEED

    def noise_generation(self, signal_power: float) -> float:
        return 1e-9 * signal_power * self.length

    def propagate(self, signal: 'signal_information'):
        latency = self.latency_generation()
        signal.update_latency(latency)

        noise = self.noise_generation(signal.get_signal_power())
        signal.update_noise_power(noise)

        if signal.get_path():
            next_node_label = signal.get_path()[0]
            next_node = self.successive.get(next_node_label)
            if next_node:
                next_node.propagate(signal)


class Network:
    def __init__(self, json_file: 'nodes.json'):
        self.nodes = {}
        self.lines = {}
        self.load_network(json_file)

    def load_network(self, json_file: 'nodes.json'):
        with open(json_file, 'r') as file:
            data = json.load(file)
            for label, info in data.items():
                node = Node({'label': label, 'position': tuple(info['position']), 'connected_nodes': info['connected_nodes']})
                self.nodes[label] = node

            for label, node in self.nodes.items():
                for connected_label in node.connected_nodes:
                    if label + connected_label not in self.lines:
                        position1 = self.nodes[label].position
                        position2 = self.nodes[connected_label].position
                        length = math.dist(position1, position2)
                        line_ab = Line(label + connected_label, length)
                        line_ba = Line(connected_label + label, length)
                        self.lines[label + connected_label] = line_ab
                        self.lines[connected_label + label] = line_ba

    def connect(self):
        for label, node in self.nodes.items():
            node.successive = {neighbor: self.lines[label + neighbor] for neighbor in node.connected_nodes if label + neighbor in self.lines}

        for line_label, line in self.lines.items():
            start_node = line_label[0]
            end_node = line_label[1]
            line.successive[end_node] = self.nodes[end_node]

    def find_paths(self, start: str, end: str, path=None):
        if path is None:
            path = [start]
        if start == end:
            return [path]

        paths = []
        for node in self.nodes[start].connected_nodes:
            if node not in path:
                new_paths = self.find_paths(node, end, path + [node])
                for new_path in new_paths:
                    paths.append(new_path)
        return paths

    def propagate(self, signal_info: signal_information) -> signal_information:
        start_node_label = signal_info.get_path()[0]
        if start_node_label in self.nodes:
            self.nodes[start_node_label].propagate(signal_info)
        return signal_info

    def draw(self):
        for label, node in self.nodes.items():
            plt.plot(*node.position, 'o', label=label)
            for connected_label in node.connected_nodes:
                pos1 = node.position
                pos2 = self.nodes[connected_label].position
                plt.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]], 'k-')
        plt.legend()
        plt.show()

    def create_dataframe(self, signal_power: float = 0.001) -> pd.DataFrame:
        data = []
        for start in self.nodes:
            for end in self.nodes:
                if start != end:
                    paths = self.find_paths(start, end)
                    for path in paths:
                        signal_info = signal_information(signal_power, path[:])
                        propagated_signal = self.propagate(signal_info)
                        if propagated_signal.get_noise_power() > 0:
                            snr_db = 10 * math.log10(propagated_signal.get_signal_power() / propagated_signal.get_noise_power())
                        else:
                            snr_db = float('inf')
                        data.append({
                            'Path': '->'.join(path),
                            'Latency (s)': propagated_signal.get_latency(),
                            'Noise Power (W)': propagated_signal.get_noise_power(),
                            'SNR (dB)': snr_db
                        })
        return pd.DataFrame(data, columns=['Path', 'Latency (s)', 'Noise Power (W)', 'SNR (dB)'])


# Main Execution
if __name__ == "__main__":
    network = Network('nodes.json')  # Ensure 'nodes.json' is in the same directory
    network.connect()  # Set up connections
    df = network.create_dataframe(signal_power=0.001)  # Create DataFrame with a given signal power
    print(df)  # Display the DataFrame
    network.draw()  # Optionally, visualize the network
