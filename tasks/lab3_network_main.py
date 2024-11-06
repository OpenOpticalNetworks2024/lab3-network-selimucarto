
import json
import math
import sys

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from core.elements import Network, signal_information


# Define paths
ROOT = Path(__file__).resolve().parent.parent
INPUT_FOLDER = ROOT / 'resources'
file_input = INPUT_FOLDER / 'resources/nodes.json'  # Full path to the JSON file
SIGNAL_POWER_W = 1e-3  # Signal power in watts (1 mW)

def main():
    # Load the network data from a JSON file (assume 'nodes.json' contains the network structure)
    network = Network('nodes.json')
    
    # Connect the nodes and lines
    network.connect()

    # Initialize an empty list to store path metrics
    data = []
    signal_power = 1e-3  # 1 mW in watts

    # Iterate over all possible pairs of nodes
    for start in network.nodes:
        for end in network.nodes:
            if start != end:
                # Find all possible paths between the start and end nodes
                paths = network.find_paths(start, end)
                for path in paths:
                    # Create a new signal_information instance with the initial signal power and path
                    signal_info = signal_information(signal_power, path.copy())
                    
                    # Propagate the signal through the network along the path
                    propagated_signal = network.propagate(signal_info)
                    
                    # Calculate metrics for the propagated signal
                    path_str = '->'.join(path)
                    latency = propagated_signal.get_latency()
                    noise_power = propagated_signal.get_noise_power()
                    snr = 10 * math.log10(signal_power / noise_power) if noise_power > 0 else float('inf')

                    # Append path information to the data list
                    data.append({
                        "Path": path_str,
                        "Total Latency (s)": latency,
                        "Total Noise Power (W)": noise_power,
                        "SNR (dB)": snr
                    })

    # Create a DataFrame from the data
    df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    df.to_csv("network_weighted_paths.csv", index=False)

    # Optionally, print the DataFrame to inspect the data
    print(df)

# Run the main function
if __name__ == "__main__":
    main()

# Load the Network from the JSON file, connect nodes and lines in Network.
# Then propagate a Signal Information object of 1mW in the network and save the results in a dataframe.
# Convert this dataframe in a csv file called 'weighted_path' and finally plot the network.
# Follow all the instructions in README.md file
