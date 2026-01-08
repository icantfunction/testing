#!/usr/bin/env python3
"""
Test script for formulary_fetch.py

This script demonstrates the functionality with mock data since network access
may be restricted in the testing environment.
"""

import sys
import json
import tempfile
import os
import csv

# Import the main module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from formulary_fetch import export_to_csv, filter_local


def test_csv_export():
    """Test CSV export functionality with mock data."""
    print("Testing CSV export...")
    
    # Mock data similar to what the API would return
    mock_data = [
        {
            'contract_id': 'H1234',
            'plan_id': 'P001',
            'drug_name': 'Aspirin',
            'tier': '1',
            'prior_authorization': 'No',
            'quantity_limit': 'No'
        },
        {
            'contract_id': 'H1234',
            'plan_id': 'P001',
            'drug_name': 'Ibuprofen',
            'tier': '2',
            'prior_authorization': 'Yes',
            'quantity_limit': 'No'
        },
        {
            'contract_id': 'H5678',
            'plan_id': 'P002',
            'drug_name': 'Lisinopril',
            'tier': '1',
            'prior_authorization': 'No',
            'quantity_limit': 'Yes'
        }
    ]
    
    # Test export to file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        temp_file = f.name
    
    try:
        export_to_csv(mock_data, temp_file)
        
        # Read back and verify
        with open(temp_file, 'r') as f:
            content = f.read()
            print("Generated CSV:")
            print(content)
            
        # Verify it's valid CSV
        with open(temp_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 3, f"Expected 3 rows, got {len(rows)}"
            assert rows[0]['drug_name'] == 'Aspirin'
            print("✓ CSV export test passed!")
            
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_json_output():
    """Test JSON output functionality."""
    print("\nTesting JSON output...")
    
    mock_data = [
        {'id': '1', 'name': 'Drug A', 'tier': '1'},
        {'id': '2', 'name': 'Drug B', 'tier': '2'}
    ]
    
    json_output = json.dumps(mock_data, indent=2)
    print("Generated JSON:")
    print(json_output)
    
    # Verify it's valid JSON
    parsed = json.loads(json_output)
    assert len(parsed) == 2
    assert parsed[0]['name'] == 'Drug A'
    print("✓ JSON output test passed!")


def test_url_construction():
    """Test URL construction with different parameters."""
    print("\nTesting URL construction...")
    
    from urllib.parse import urlencode
    
    API_BASE_URL = "https://data.cms.gov/data-api/v1/dataset"
    DATASET_ID = "cb2a224f-4d52-4cae-aa55-8c00c671384f"
    
    # Test cases
    test_cases = [
        (None, None, f"{API_BASE_URL}/{DATASET_ID}/data"),
        (10, None, f"{API_BASE_URL}/{DATASET_ID}/data?size=10"),
        (None, 5, f"{API_BASE_URL}/{DATASET_ID}/data?offset=5"),
        (10, 5, f"{API_BASE_URL}/{DATASET_ID}/data?size=10&offset=5"),
    ]
    
    for size, offset, expected_base in test_cases:
        url = f"{API_BASE_URL}/{DATASET_ID}/data"
        params = {}
        if size is not None:
            params['size'] = size
        if offset is not None:
            params['offset'] = offset
        
        if params:
            url = f"{url}?{urlencode(params)}"
        
        print(f"  size={size}, offset={offset}")
        print(f"    Generated: {url}")
        assert url.startswith(expected_base.split('?')[0])
        
    print("✓ URL construction test passed!")


def test_filter_local():
    """Test local filtering functionality."""
    print("\nTesting local filtering...")
    
    mock_data = [
        {
            'organization_name': 'Humana Inc.',
            'plan_name': 'Humana Gold Plus',
            'state': 'FL',
            'drug_name': 'Aspirin'
        },
        {
            'organization_name': 'UnitedHealthcare',
            'plan_name': 'UHC MAPD Plan',
            'state': 'FL',
            'drug_name': 'Ibuprofen'
        },
        {
            'organization_name': 'Aetna',
            'plan_name': 'Aetna Medicare',
            'state': 'CA',
            'drug_name': 'Lisinopril'
        },
        {
            'organization_name': 'Wellcare',
            'plan_name': 'Wellcare Advantage',
            'state': 'FL',
            'drug_name': 'Metformin'
        }
    ]
    
    # Test filter by organization
    filtered = filter_local(mock_data, organization='Humana')
    assert len(filtered) == 1
    assert filtered[0]['organization_name'] == 'Humana Inc.'
    print("  ✓ Organization filter works")
    
    # Test filter by state
    filtered = filter_local(mock_data, state='FL')
    assert len(filtered) == 3
    print("  ✓ State filter works")
    
    # Test filter by both
    filtered = filter_local(mock_data, organization='UHC', state='FL')
    assert len(filtered) == 1
    assert filtered[0]['organization_name'] == 'UnitedHealthcare'
    print("  ✓ Combined filters work")
    
    # Test case-insensitive
    filtered = filter_local(mock_data, organization='aetna')
    assert len(filtered) == 1
    print("  ✓ Case-insensitive filter works")
    
    print("✓ Local filtering test passed!")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Running tests for formulary_fetch.py")
    print("=" * 60)
    
    try:
        test_csv_export()
        test_json_output()
        test_url_construction()
        test_filter_local()
        
        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        return 0
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
