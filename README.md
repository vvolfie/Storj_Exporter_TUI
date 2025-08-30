# Storj Exporter TUI

A Python **Terminal User Interface (TUI)** for the Storj Exporter by **anclrii**.  
Work-in-progress.

## Overview

Provides an interactive terminal-based interface to view metrics collected by the Storj Exporter. Ideal for quick, local node monitoring without needing a browser or Grafana.

## Requirements

- Python 3.x  
- A running **Storj Exporter** instance (e.g., [`anclrii/storj-exporter`](https://github.com/anclrii/Storj-Exporter)).
- Network access to the exporter’s metrics endpoint (default: `http://localhost:9651`).

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/vvolfie/Storj_Exporter_TUI.git
    cd Storj_Exporter_TUI
    ```

2. (Optional) Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies (if any are listed in `requirements.txt`; otherwise skip this step):
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the TUI:
```bash
python tui.py
