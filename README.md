# CMS Prescription Drug Plan Formulary Fetcher

A Python script to fetch Monthly Prescription Drug Plan Formulary & Pharmacy Network data from the CMS (Centers for Medicare & Medicaid Services) data API.

## Dataset Information

- **Dataset ID**: cb2a224f-4d52-4cae-aa55-8c00c671384f
- **Source**: CMS Data API (catalog.data.gov)
- **API Endpoint**: https://data.cms.gov/data-api/v1/dataset/cb2a224f-4d52-4cae-aa55-8c00c671384f/data

## Requirements

- Python 3.6 or higher
- No external dependencies (uses Python standard library only)

## Installation

Clone the repository:
```bash
git clone https://github.com/icantfunction/testing.git
cd testing
```

Make the script executable (optional):
```bash
chmod +x formulary_fetch.py
```

## Usage

### Basic Usage

Fetch all available data and output to CSV (stdout):
```bash
python3 formulary_fetch.py
```

### Pagination

Retrieve a specific number of records:
```bash
python3 formulary_fetch.py --size 100
```

Retrieve records starting from a specific offset:
```bash
python3 formulary_fetch.py --size 100 --offset 200
```

### Output Options

Save to a CSV file:
```bash
python3 formulary_fetch.py --size 100 --output formulary_data.csv
```

Output as JSON instead of CSV:
```bash
python3 formulary_fetch.py --size 10 --json
```

Save JSON to a file:
```bash
python3 formulary_fetch.py --size 100 --json --output formulary_data.json
```

### Command-Line Options

- `--size SIZE`: Number of records to retrieve
- `--offset OFFSET`: Starting position for pagination
- `--output OUTPUT, -o OUTPUT`: Output file path (default: stdout)
- `--json`: Output as JSON instead of CSV
- `--help, -h`: Show help message

## Examples

1. Fetch the first 50 records and save to CSV:
   ```bash
   python3 formulary_fetch.py --size 50 --output sample.csv
   ```

2. Fetch records 100-150:
   ```bash
   python3 formulary_fetch.py --size 50 --offset 100 --output page2.csv
   ```

3. Preview 10 records as JSON:
   ```bash
   python3 formulary_fetch.py --size 10 --json
   ```

## License

This project is provided as-is for accessing publicly available CMS data.