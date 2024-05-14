# LLM-integration

## Overview

This project uses a Large Language Model (LLM) to analyze the unit price data and provide feedback on individual sales representatives, overall team performance, and sales trends. The backend system is developed using Flask and integrates Cohere's LLM for data analysis.

## Features

- **Data Ingestion**: Supports uploading sales data in JSON Format.
- **LLM Integration**: Uses Cohere's LLM to generate qualitative feedback and actionable insights 
- **API Endpoints**:
  - `/api/top_unit`: Provides Detail feedback on overall units and also the best unit.
  - `/api/unit_price_history`: Finds units with the biggest price changes downwards.
  - `/api/building_deals`: Finds the best building deals in a specified neighborhood.
  - `/api/sales_rep_feedback`: Provides performance feedback for a specific sales representative.
  - `/api/team_performance`: Assesses overall team performance.

## Setup

1. Clone the repository:
    ```
    git clone https://github.com/muhammadbahjat/LLM-integration.git
    ```

3. Set your Cohere API key:
    login into Cohere and get your API 

4. RUN Flask App:
```
   python app.py
```



## Usage

Use Postman or any API testing tool to interact with the endpoints. Examples:
- Upload JSON data on home.html:
- URL: `http://127.0.0.1:5500/home.html` or if Using Postman
- Method: POST

- URL: `http://127.0.0.1:5000/upload`
- Body: Form-data with key `file` and value as the JSON file.

- Get feedback for the best unit:
- Method: GET
- URL: `http://127.0.0.1:5000/api/top_unit`

- Get units with the biggest price changes downwards:
- Method: GET
- URL: `http://127.0.0.1:5000/api/unit_price_history`

- Get best building deals in a specified neighborhood:
- Method: GET
- URL: `http://127.0.0.1:5000/api/building_deals`

- Get feedback for a specific sales representative:
- Method: GET
- URL: `http://127.0.0.1:5000/api/sales_rep_feedback?rep_id=1`

- Get overall team performance:
- Method: GET
- URL: `http://127.0.0.1:5000/api/team_performance`

## Architecture and Technologies Used

- **Backend**: Flask
- **LLM Integration**: Cohere
- **Data Formats**: JSON (Converting to CSV)

## License

This project is licensed under the MIT License.
