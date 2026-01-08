#!/usr/bin/env python3
"""
Fetch MAPD formulary data for specific organizations in Florida.

This script fetches formulary information for Devoted, UHC, Humana, Wellcare, 
and Aetna MAPD plans in Florida.
"""

import sys
import os

# Import from the main module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from formulary_fetch import fetch_formulary_data, filter_local, export_to_csv


# Organizations to fetch
ORGANIZATIONS = [
    'Devoted',
    'UHC',
    'United',
    'UnitedHealthcare',
    'Humana',
    'Wellcare',
    'Aetna'
]

STATE = 'FL'
BATCH_SIZE = 1000
MAX_RECORDS_PER_ORG = 5000  # Limit to prevent excessive API calls


def main():
    """Fetch formulary data for specified organizations in Florida."""
    print(f"Fetching MAPD formulary data for Florida organizations...", file=sys.stderr)
    print(f"Organizations: {', '.join(ORGANIZATIONS)}", file=sys.stderr)
    print(f"State: {STATE}", file=sys.stderr)
    print("", file=sys.stderr)
    
    all_results = []
    
    for org in ORGANIZATIONS:
        print(f"Fetching data for {org}...", file=sys.stderr)
        
        try:
            # Fetch data in batches
            offset = 0
            org_records = []
            
            while True:
                data = fetch_formulary_data(size=BATCH_SIZE, offset=offset)
                
                if not data:
                    break
                
                # Filter by organization and state
                filtered = filter_local(data, organization=org, state=STATE)
                org_records.extend(filtered)
                
                print(f"  Batch {offset // BATCH_SIZE + 1}: {len(filtered)} matching records", file=sys.stderr)
                
                # If we got fewer records than batch_size, we've reached the end
                if len(data) < BATCH_SIZE:
                    break
                
                offset += BATCH_SIZE
                
                # Limit to prevent excessive API calls
                if offset >= MAX_RECORDS_PER_ORG:
                    print(f"  Reached fetch limit of {MAX_RECORDS_PER_ORG} records", file=sys.stderr)
                    break
            
            print(f"  Total for {org}: {len(org_records)} records", file=sys.stderr)
            all_results.extend(org_records)
            
        except Exception as e:
            print(f"  Error fetching data for {org}: {e}", file=sys.stderr)
            continue
    
    print("", file=sys.stderr)
    print(f"Total records found: {len(all_results)}", file=sys.stderr)
    
    if all_results:
        # Export to CSV
        output_file = "florida_mapd_formulary.csv"
        export_to_csv(all_results, output_file)
        print(f"Data exported to: {output_file}", file=sys.stderr)
    else:
        print("No matching records found", file=sys.stderr)


if __name__ == '__main__':
    main()
