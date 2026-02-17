# Supplier Evaluation System

A Python-based tool for evaluating and ranking suppliers based on configurable criteria, with a modern web interface.

## Features

- **Supplier Validation**: Validates supplier data against strict Pydantic models.
- **Scoring & Ranking**: diverse criteria including cost, region, and performance history.
- **Risk Assessment**: Automatically calculates risk levels based on performance scores and regional diversity.
- **Web Interface**:
    - Rank suppliers based on custom inputs (Volume, Region, Cost).
    - View all suppliers.
    - Detailed breakdown of supplier capabilities, pricing, and history via modal.
- **API**: RESTful API powered by FastAPI.

## Tech Stack

- **Backend**: Python 3.9+, FastAPI, Pydantic
- **Frontend**: HTML5, Vanilla JavaScript, CSS (Glassmorphism design)
- **Testing**: Pytest

## Setup

1.  **Clone the repository** (or navigate to the project directory):
    ```bash
    cd path/to/supplier_evaluation
    ```

2.  **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install fastapi uvicorn pydantic
    ```

## Usage

1.  **Start the Server**:
    Run the following command to start the FastAPI server with hot-reloading enabled:
    ```bash
    uvicorn main:app --reload
    ```

2.  **Access the Application**:
    Open your web browser and navigate to:
    [http://localhost:8000](http://localhost:8000)

3.  **Evaluate Suppliers**:
    - **Rank**: Enter your requirements (Component, Volume, Region, Target Cost) and click "Rank Suppliers".
    - **View All**: Click "View All" to see the complete list of available suppliers.
    - **Details**: Click on any row in the results table to view comprehensive details for that supplier.

## Project Structure

- `main.py`: Application entry point and API endpoints.
- `models.py`: Data models defining Supplier, Region, Cost, etc.
- `scoring.py`: Logic for calculating fit scores.
- `ranking.py`: Logic for sorting and ranking suppliers.
- `index.html`: Frontend user interface.
- `supplier_schema.json`: JSON schema for supplier data validation.
