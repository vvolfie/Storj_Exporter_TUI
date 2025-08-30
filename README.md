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
```
## Screenshots
<img width="1691" height="685" alt="{AB2A3753-A017-47D0-9111-8FFB95DF5E83}" src="https://github.com/user-attachments/assets/e65253a5-8c08-4c54-9ede-915abfb2f541" />

<img width="1690" height="681" alt="{ABA4B0D5-EAD1-41A9-8833-EBC95D325A22}" src="https://github.com/user-attachments/assets/57fca71e-d772-42ce-9e7f-e88087c49dc8" />

<img width="1691" height="678" alt="{9914880E-81EB-4960-8950-0BE389C09869}" src="https://github.com/user-attachments/assets/c97f4125-5833-4ed1-a937-bd5f2b7b47c2" />

