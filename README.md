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

## Evaluation Logic

The system ranks suppliers by calculating a **Fit Score** (0-100) based on four weighted criteria:

1.  **Capability Match (40%)**: Does the supplier offer the specific service you need?
    -   *Example*: If you require "CNC Machining" and the supplier lists it, they receive a 100% capability score. If not, 0%.
2.  **Cost Alignment (30%)**: Is their price within your target range?
    -   *High Match*: Price <= Target (e.g., Target $10, Supplier $9 → 100% score)
    -   *Medium Match*: Price within 10% of Target (e.g., Target $10, Supplier $10.50 → 50% score)
    -   *Low/No Match*: Price > Target + 10% (e.g., Target $10, Supplier $12 → 0% score)
3.  **Region Match (20%)**: Are they located in your target country/state?
    -   *Example*: If you target "USA" and the supplier has operations in "USA", they get a 100% region score.
4.  **Performance History (10%)**: Based on their average quality, timeliness, and communication scores.
    -   *Example*: A supplier with an overall rating of 9.0/10 contributes 9 points to the final weighted score.

### Risk Assessment

Risk is automatically categorized as **Low**, **Medium**, or **High** based on the worst of two factors:
-   **Performance Risk**: Derived from their historical performance scores.
-   **Geographic Risk**: Based on how many countries they operate in (more countries = lower risk).

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
