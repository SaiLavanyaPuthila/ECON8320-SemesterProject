# ECON8320 Semester Project

Welcome to the **ECON8320 Semester Project** repository. This project is focused on analyzing economic data, generating insightful visualizations, and creating an interactive dashboard to showcase the results. 

## Table of Contents

- [ECON8320 Semester Project](#econ8320-semester-project)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Features](#features)
  - [Project Structure](#project-structure)
  - [Setup and Installation](#setup-and-installation)
  - [Usage](#usage)
  - [Dependencies](#dependencies)

## Project Overview

This repository contains scripts and resources for:

- Fetching and processing economic data.
- Analyzing datasets to extract meaningful insights.
- Visualizing data through an interactive Streamlit dashboard.

The project leverages Python libraries to ensure efficient data handling and intuitive presentation.

## Features

- **Automated Data Fetching**: Retrieve data from BLS API seamlessly.
- **Interactive Dashboard**: Built using Streamlit for real-time exploration.
- **Comprehensive Visualizations**: High-quality plots for data analysis.
- **Scalable Architecture**: Modular structure to facilitate extensions and improvements.

## Project Structure

```plaintext
ECON8320-SemesterProject/
├── data/                 # Contains datasets used for analysis.
├── logs/                 # Execution logs for tracking.
├── plots/                # Generated plots and visualizations.
├── fetch_data.py         # Script for data fetching.
├── main.py               # Data processing and analysis script.
├── streamlit_dashboard.py# Interactive Streamlit dashboard.
├── requirements.txt      # Project dependencies.

```

## Setup and Installation

To set up the project locally, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/SaiLavanyaPuthila/ECON8320-SemesterProject.git
    cd ECON8320-SemesterProject
    ```

2. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Streamlit dashboard:**

    ```bash
    streamlit run streamlit_dashboard.py
    ```

## Usage

1. **Data Fetching**: Use `fetch_data.py` to retrieve the necessary datasets.
2. **Data Processing**: Run `main.py` to process and analyze the data.
3. **Visualization**: Launch `streamlit_dashboard.py` to interact with the visualized results.

## Dependencies

The project requires the following Python libraries:

- Python 3.12
- `streamlit`
- `pandas`
- `numpy`
- `matplotlib`
- `plotly`



---
