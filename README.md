# Data Ingestion Platform

## Description
This data ingestion platform streamlines data collection from various departments (e.g., marketing, sales, operations) within an organization. Designed for departments without dedicated technical staff, it enables easy data contribution via CSV uploads through a user-friendly web interface. The platform ensures data quality through schema validation.

## Setup (using Docker Compose)

1. Ensure Docker and Docker Compose are installed on your system.
2. Clone this repository to your local machine.
3. Navigate to the project directory in your terminal.
4. Start the application using:

```bash
docker compose up --build -d
```

This command builds the Docker image and starts the application containers.



## Usage

1.  **Access the Web Interface:** Once the application is running (see Setup), open your web browser and navigate to `http://localhost:5000`.
    *   **Schema Overview:** The Data Team manages the expected schema for each table.
        ![page1](/docs/page1.png)

2.  **Upload CSV Files:**
    *   Click the "Choose File" button to select a CSV file from your local machine.
    *   Click the "Validate" button to submit the file.

3.  **Data Validation:** The platform validates the uploaded data against a predefined schema.
    *   **Validation and Preview:** Uploaded CSV files are validated against the schema, and a preview is displayed.
    *   If the data is valid, a success message will be displayed. If the data is invalid, an error message will be displayed.
        ![validation_success](/docs/validation_success.png)
        ![validation_failed](/docs/validation_failed.png)
    *   **Different Schemas:** The platform supports different schemas for different tables.
        ![different_schema_tables](/docs/different_schema_tables.png)

## Limitations

Please note the following limitations:

1. This is a proof-of-concept project and many features are still under development.
2. Data validation currently checks only the first ten entries. (Consider validating all entries for comprehensive data quality.)
3. Supported data types are limited to: `str`, `int`, `float`, `datetime`(YYYY-MM-DD HH:mm:ss), and `date` (YYYY-MM-DD). (Expanding data type support would increase flexibility.)
4. Files are currently stored locally. (Future enhancements may include cloud storage integration (e.g., S3 or GCS) or integration with external APIs to create an automated data pipeline.)
5. Currently, there is no account management. (Implementing user accounts would enhance security and data access control.)
