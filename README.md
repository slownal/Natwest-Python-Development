# Report Generator Microservice

A Django-based microservice for generating reports by processing input files with reference data and configurable transformation rules.

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## Using the Web Interface

The easiest way to use the application is through the web interface:

1. Open your browser and go to http://127.0.0.1:8000/api/
2. Click "Log in" in the top right corner and enter your admin credentials
3. After logging in, you'll see the API root page with links to:
   - Reports
   - Configurations

### Creating a Configuration
1. Click on "Configurations"
2. Click the "POST" button
3. Fill in the form:
   - Name: test_config
   - Config file: Select the example_config.json file from media/configs/
   - Click "POST" to submit

### Creating a Report
1. Click on "Reports"
2. Click the "POST" button
3. Fill in the form:
   - Name: test_report
   - Input file: Select example_input.csv from media/input_files/
   - Reference file: Select example_reference.csv from media/reference_files/
   - Config: Select the configuration you created
   - Click "POST" to submit

### Generating a Report
1. Click on the specific report you want to generate
2. Click the "POST" button next to "generate_report"
3. Click "POST" to confirm

## API Endpoints

### Report Configurations
- `GET /api/configs/` - List all configurations
- `POST /api/configs/` - Create a new configuration
- `GET /api/configs/{id}/` - Get a specific configuration
- `PUT /api/configs/{id}/` - Update a configuration
- `DELETE /api/configs/{id}/` - Delete a configuration

### Reports
- `GET /api/reports/` - List all reports
- `POST /api/reports/` - Create a new report
- `GET /api/reports/{id}/` - Get a specific report
- `PUT /api/reports/{id}/` - Update a report
- `DELETE /api/reports/{id}/` - Delete a report
- `POST /api/reports/{id}/generate_report/` - Generate a report

## Example Configuration File

Create a JSON file with the following structure:
```json
{
    "rules": [
        {
            "output_field": "outfield1",
            "operation": "concat",
            "input_fields": ["field1", "field2"]
        },
        {
            "output_field": "outfield2",
            "operation": "reference",
            "input_fields": ["refdata1"]
        },
        {
            "output_field": "outfield3",
            "operation": "concat",
            "input_fields": ["refdata2", "refdata3"]
        },
        {
            "output_field": "outfield4",
            "operation": "multiply_max",
            "input_fields": ["field3", "field5", "refdata4"]
        },
        {
            "output_field": "outfield5",
            "operation": "max",
            "input_fields": ["field5", "refdata4"]
        }
    ]
}
```

## File Requirements

### Input File (input.csv)
- Columns: field1(String), field2(String), field3(String), field4(String), field5(Decimal), refkey1(String), refkey2(String)

### Reference File (reference.csv)
- Columns: refkey1(String), refdata1(String), refkey2(String), refdata2(String), refdata3(String), refdata4(Decimal)

### Output File (output.csv)
- Columns: outfield1, outfield2, outfield3, outfield4, outfield5

## Example Files

The project includes example files in the media directory:
- `media/configs/example_config.json` - Example configuration file
- `media/input_files/example_input.csv` - Example input file
- `media/reference_files/example_reference.csv` - Example reference file

## Authentication

The API uses Django's session authentication. You need to:
1. Log in through the admin interface or
2. Use basic authentication with your credentials

## Features

- Web interface for easy interaction
- REST API for programmatic access
- Configurable transformation rules
- Support for large files (up to 1GB)
- Authentication and authorization
- File upload and download
- Report generation on demand 