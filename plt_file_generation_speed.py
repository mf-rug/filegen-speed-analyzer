import os
import matplotlib.pyplot as plt
from datetime import datetime
from typing import List, Tuple
import argparse

def get_file_timestamps(folder: str, extension: str, timestamp_type: str) -> List[Tuple[str, float]]:
    files = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.endswith(extension) and os.path.isfile(os.path.join(folder, f))
    ]

    if timestamp_type == "creation":
        timestamps = [(f, os.stat(f).st_birthtime) for f in files]
    elif timestamp_type == "modification":
        timestamps = [(f, os.path.getmtime(f)) for f in files]
    else:
        raise ValueError("Invalid timestamp_type. Use 'creation' or 'modification'.")

    return sorted(timestamps, key=lambda x: x[1])

def segment_file_batches(timestamps: List[Tuple[str, float]], gap_factor: float = 5.0) -> List[List[Tuple[str, float]]]:
    if len(timestamps) < 2:
        return [timestamps]

    # Get list of deltas
    gaps = [timestamps[i+1][1] - timestamps[i][1] for i in range(len(timestamps) - 1)]
    typical_gap = sorted(gaps)[len(gaps) // 2]  # median

    threshold = gap_factor * typical_gap
    batches = []
    current_batch = [timestamps[0]]

    for i in range(1, len(timestamps)):
        if timestamps[i][1] - timestamps[i-1][1] > threshold:
            batches.append(current_batch)
            current_batch = [timestamps[i]]
        else:
            current_batch.append(timestamps[i])

    if current_batch:
        batches.append(current_batch)

    return batches

def plot_file_generation_speed(
    folder: str,
    extension: str,
    window_size: int,
    time_unit: str = "minute",  # "second", "minute", "hour"
    timestamp_type: str = "creation",  # "creation" or "modification"
    gap_factor: float = 5.0
):
    unit_to_seconds = {"second": 1, "minute": 60, "hour": 3600}
    if time_unit not in unit_to_seconds:
        raise ValueError("Invalid time_unit. Choose from 'second', 'minute', 'hour'.")

    timestamps = get_file_timestamps(folder, extension, timestamp_type)
    batches = segment_file_batches(timestamps, gap_factor=gap_factor)

    colors = plt.cm.get_cmap("tab10", len(batches))
    plt.figure(figsize=(10, 5))

    for idx, batch in enumerate(batches):
        if len(batch) < window_size:
            continue  # skip too-small batches

        times = []
        rates = []
        for i in range(len(batch) - window_size + 1):
            window = batch[i:i + window_size]
            t_start = window[0][1]
            t_end = window[-1][1]
            delta = t_end - t_start
            if delta == 0:
                rate = float('inf')
            else:
                rate = window_size / (delta / unit_to_seconds[time_unit])
            midpoint = (t_start + t_end) / 2
            times.append(datetime.fromtimestamp(midpoint))
            rates.append(rate)

        plt.plot(times, rates, marker='o', label=f'Batch {idx + 1}', color=colors(idx))

    plt.xlabel("Time (midpoint of window)")
    plt.ylabel(f"Files per {time_unit}")
    plt.title(f"File generation speed ({window_size}-file window, {timestamp_type})")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# === Execute with default values ===

if __name__ == "__main__":
    folder = os.getcwd()
    extension = ".sim"
    window_size = 100
    time_unit = "hour"
    timestamp_type = "creation"  # or "modification"
    gap_factor = 5.0


    def parse_args():
        parser = argparse.ArgumentParser(description='Plot file generation speed over time.')
        parser.add_argument('-f', '--folder', default=os.getcwd(),
                          help='Folder to analyze (default: current directory)')
        parser.add_argument('-e', '--extension', default='.sim',
                          help='File extension to analyze (default: .sim)')
        parser.add_argument('-w', '--window-size', type=int, default=100,
                          help='Window size for rate calculation (default: 100)')
        parser.add_argument('-u', '--time-unit', default='hour',
                          choices=['second', 'minute', 'hour'],
                          help='Time unit for rate calculation (default: hour)')
        parser.add_argument('-t', '--timestamp-type', default='creation',
                          choices=['creation', 'modification'],
                          help='Type of timestamp to use (default: creation)')
        parser.add_argument('-g', '--gap-factor', type=float, default=5.0,
                          help='Factor for determining batch gaps (default: 5.0)')
        return parser.parse_args()

    if __name__ == "__main__":
        args = parse_args()
        plot_file_generation_speed(
            args.folder,
            args.extension,
            args.window_size,
            args.time_unit,
            args.timestamp_type,
            args.gap_factor
        )
