# fern-humidity-regressor

> A machine learning utility that forecasts optimal watering intervals for indoor ferns using ambient room temperature and humidity sensor streams.

---

## Overview

Indoor fern care often suffers from inconsistent watering schedules driven by fluctuating indoor microclimates. Manual estimation fails when ambient temperature and humidity shifts alter soil evaporation rates. This tool solves that operational friction by training a supervised linear regression model on historical sensor averages, translating environmental telemetry into precise, data-backed watering intervals.

## How It Works

1. **Telemetry Ingestion:** The script initializes a local TCP socket server listening for incoming JSON data packets containing temperature and humidity values.
2. **Fallback Execution:** If no network socket connection is established within a defined timeout window (2.0 seconds), the execution thread gracefully transitions to manual terminal inputs.
3. **Regression Modeling:** Input parameters are structured into two-dimensional feature arrays and evaluated against coefficients trained via scikit-learn's `LinearRegression` estimator.
4. **Validation & Output:** Input values undergo strict boundary validation before outputting the predicted watering timeline in days.

## Key Features

* **Dual-Mode Data Ingestion:** Accepts real-time sensor packets over TCP sockets or interactive console inputs.
* **Supervised Learning Engine:** Utilizes scikit-learn regression to model inverse temperature-humidity moisture loss.
* **Defensive Error Handling:** Includes bounds-checking for physical sensor ranges and non-blocking socket timeouts to prevent runtime crashes.
* **Standard Library Integration:** Minimizes external bloat by leaning on native Python primitives where applicable.

## Tech Stack & Core Dependencies Breakdown

* **Python 3.10+:** Core runtime environment.
* **`socket` (Standard Library):** Manages local TCP server binding and incoming network data streams.
* **`json` (Standard Library):** Parses incoming network telemetry payloads.
* **`sys` (Standard Library):** Manages safe terminal exits and exit status codes.
* **`scikit-learn`:** Provides the `LinearRegression` algorithm used for continuous target prediction.
* **`numpy`:** Handles numerical array operations and multidimensional feature matrices.

## Environment & Web-Based Quick Start

### Setup via GitHub Codespaces or Local Terminal

1. **Clone or open the repository** in your preferred Python environment.
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install dependencies:**
    ```bash
    pip install scikit-learn numpy
    ```
4. **Execute the script:**
    ```bash
    python plant_predictor.py
    ```

## Repository Structure
```bash
fern-humidity-regressor/
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── README.md
└── main.py
```

## Roadmap

**[ ]** AsyncIO Migration: Transition the synchronous socket listener to asyncio for non-blocking concurrent sensor stream handling.

**[ ]** SQLite Logging: Implement persistent local storage to record historical sensor logs and improve model retraining over time.

**[ ]** Type Stubs & Linter Integration: Add strict type hints (mypy) and automated code formatting enforcement.