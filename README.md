# File Generation Speed Plotter

This script analyzes the creation or modification times of files in a directory and visualizes the rate at which files are generated over time. It is useful for understanding the throughput of file-producing processes, such as simulations, data pipelines, or logging systems.

## Features

- Plots the rate of file generation using a sliding window.
- Supports grouping files into batches based on time gaps.
- Customizable time units (seconds, minutes, hours).
- Choose between file creation or modification timestamps.
- Command-line interface with flexible options.

## Requirements

- Python 3.7+
- matplotlib

Install dependencies with:

```bash
pip install matplotlib
```

## Usage

```bash
python plt_file_generation_speed.py [options]
```

### Options

| Option                    | Description                                                      | Default         |
|---------------------------|------------------------------------------------------------------|-----------------|
| `-f`, `--folder`          | Folder to analyze                                                | Current dir     |
| `-e`, `--extension`       | File extension to analyze                                        | `.sim`          |
| `-w`, `--window-size`     | Window size for rate calculation (number of files per window)    | 100             |
| `-u`, `--time-unit`       | Time unit for rate calculation (`second`, `minute`, `hour`)      | `hour`          |
| `-t`, `--timestamp-type`  | Type of timestamp to use (`creation`, `modification`)            | `creation`      |
| `-g`, `--gap-factor`      | Factor for determining batch gaps (higher = fewer, larger batches)| 5.0             |

### Example

```bash
python plt_file_generation_speed.py -f ./output -e .log -w 50 -u minute -t modification -g 3.0
```

This command analyzes `.log` files in the `./output` directory, using a window size of 50 files, rates per minute, modification timestamps, and a gap factor of 3.0.

## How It Works

- The script collects timestamps for all files matching the given extension.
- Files are grouped into batches if there are large time gaps between them (configurable).
- For each batch, it computes the file generation rate using a sliding window.
- The result is plotted as a time series, showing how the file generation speed changes over time.

## License

MIT License
