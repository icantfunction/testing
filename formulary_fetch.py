#!/usr/bin/env python3
"""
Fetch Monthly Prescription Drug Plan Formulary & Pharmacy Network data from CMS API.

This script retrieves data from the CMS data API and can export it to CSV format.
Dataset: cb2a224f-4d52-4cae-aa55-8c00c671384f
"""

import argparse
import csv
import json
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode


API_BASE_URL = "https://data.cms.gov/data-api/v1/dataset"
DATASET_ID = "cb2a224f-4d52-4cae-aa55-8c00c671384f"


def fetch_formulary_data(size=None, offset=None):
    """
    Fetch formulary data from CMS API.
    
    Args:
        size (int, optional): Number of records to retrieve
        offset (int, optional): Starting position for pagination
        
    Returns:
        list: List of records from the API
    """
    url = f"{API_BASE_URL}/{DATASET_ID}/data"
    
    # Build query parameters
    params = {}
    if size is not None:
        params['size'] = size
    if offset is not None:
        params['offset'] = offset
    
    if params:
        url = f"{url}?{urlencode(params)}"
    
    try:
        print(f"Fetching data from: {url}", file=sys.stderr)
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        
        with urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
    except HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"URL Error: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)


def export_to_csv(data, output_file=None):
    """
    Export data to CSV format.
    
    Args:
        data (list): List of records to export
        output_file (str, optional): Output file path. If None, writes to stdout
    """
    if not data:
        print("No data to export", file=sys.stderr)
        return
    
    # Get all unique field names from all records
    fieldnames = set()
    for record in data:
        fieldnames.update(record.keys())
    fieldnames = sorted(fieldnames)
    
    # Determine output destination
    if output_file:
        output = open(output_file, 'w', newline='', encoding='utf-8')
    else:
        output = sys.stdout
    
    try:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    finally:
        if output_file:
            output.close()


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Fetch CMS Monthly Prescription Drug Plan Formulary data'
    )
    parser.add_argument(
        '--size',
        type=int,
        help='Number of records to retrieve'
    )
    parser.add_argument(
        '--offset',
        type=int,
        help='Starting position for pagination'
    )
    parser.add_argument(
        '--output',
        '-o',
        help='Output CSV file (default: stdout)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON instead of CSV'
    )
    
    args = parser.parse_args()
    
    # Fetch data
    data = fetch_formulary_data(size=args.size, offset=args.offset)
    
    # Output data
    if args.json:
        output_data = json.dumps(data, indent=2)
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output_data)
        else:
            print(output_data)
    else:
        export_to_csv(data, args.output)
    
    # Print summary to stderr
    print(f"Retrieved {len(data)} records", file=sys.stderr)


if __name__ == '__main__':
    main()
