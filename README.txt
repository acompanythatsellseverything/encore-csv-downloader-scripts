# CSV to Strapi Data Uploader
These scripts provide a way to upload data from CSV files directly to Strapi via its admin API. The system consists of two main components:

1. CSV Upload Server: A local HTTP server for handling file uploads.
2. CSV Data Processor: A script that watches a directory for CSV files, processes them, and sends the data to Strapi.

## Prerequisites
- Python 3.x
- Strapi (v5.0.0 or higher recommended)
- Required Python packages (install via pip install -r requirements.txt):
  - pandas
  - requests
  - python-dotenv
- Environment variables configured in a .env file (explained below)

## Setup
1. Clone or download the repository with these scripts to your local machine.
2. Configure the .env file with the following variables:
  - WATCH_DIR: Directory to watch for new CSV files
  - STRAPI_URL: Strapi endpoint URL (e.g., https://yourdomain.com/api/articles)
  - TOKEN: Strapi API authentication token
  - EVENT_TYPE_MAPPING: Mappings of event type names to IDs, e.g., Concert:1,Workshop:2
3. Run the upload csv:

        _python upload_csv.py_

4. This server runs on port 8000 by default and allows you to upload files to the watch directory.

5. Start the CSV Data Processor:

        _python send_data.py_

## Usage
### 1. CSV Upload Server
The upload_server.py script starts a simple HTTP server. It can receive file uploads with a POST request to /, where the file should be attached as multipart/form-data with the field name file.

- Start the server:

        _python upload_server.py_

- Upload a file via POST request:

        _POST http://localhost:8000/_
        _Content-Type: multipart/form-data
        _Body:
        _file: [CSV file]
The server saves files in the directory where the script is located.

### 2. CSV Data Processor
The send_data.py script continuously monitors the specified directory for CSV files. When a new CSV file is detected, the script:

Parses and formats the data
Sends the formatted data to Strapi using the configured API endpoint
Deletes the CSV file once processed
File Format
The CSV should contain the following columns:

title, description, slug, event_type, metaTitle, metaDescription, metaKeywords, cover, stay_ahead, city, date
Script Details
File Watching: The script continuously monitors WATCH_DIR and processes CSV files found in the directory.
Data Processing: Data is formatted to match Strapi's expected format. The date field is converted from DD.MM.YYYY to YYYY-MM-DD if provided.
Data Uploading: Each row is uploaded to Strapi using the API endpoint specified by STRAPI_URL.
## Example
Place your .csv files in the WATCH_DIR and run the script. The script will automatically detect, process, and upload the data to Strapi, then delete the file.

## Notes
Ensure the .env file is configured with accurate API details.
Use a reverse proxy for secure connections if deploying to a production environment.