import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# Exercise Lab3: Network

ROOT = Path(__file__).parent.parent
INPUT_FOLDER = ROOT / 'resources'
file_input = INPUT_FOLDER / 'nodes.json'

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
# Load the Network from the JSON file, connect nodes and lines in Network.
# Then propagate a Signal Information object of 1mW in the network and save the results in a dataframe.
# Convert this dataframe in a csv file called 'weighted_path' and finally plot the network.
# Follow all the instructions in README.md file
