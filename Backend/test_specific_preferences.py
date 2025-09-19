#!/usr/bin/env python3
"""
Test script for the new specific preferences route.
This demonstrates how to use the new endpoint with the provided JSON data.
"""

import requests
import json

# Base URL for the API (adjust as needed)
BASE_URL = "http://localhost:5000"

def test_specific_preferences():
    """Test the new specific preferences endpoint"""
    
    # Sample client ID (you'll need to create a client first)
    client_id = 1
    
    # Example 1: Using direct preference fields
    print("=== Test 1: Direct preference fields ===")
    direct_preferences = {
        "preferred_neighborhood": "NridgHt",
        "preferred_condition1": "Norm",
        "preferred_house_style": "2Story",
        "min_year_built": 2000,
        "max_year_built": 2010,
        "min_lot_area": 10000.0,
        "max_lot_area": 15000.0,
        "min_gr_liv_area": 1500.0,
        "max_gr_liv_area": 2000.0,
        "min_bedroom_abv_gr": 3,
        "max_bedroom_abv_gr": 4,
        "min_full_bath": 2,
        "max_full_bath": 3,
        "min_sale_price": 200000.0,
        "max_sale_price": 300000.0,
        "preferred_sale_type": "WD"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/clients/{client_id}/preferences/specific",
            json=direct_preferences,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Using the provided JSON data
    print("=== Test 2: Using provided JSON data ===")
    json_data = {
        "TotalSF": 3616.0,
        "OverallQual": 8.0,
        "OverallCond": 5.0,
        "GrLivArea": 1822.0,
        "Neighborhood": "NridgHt",
        "TotalBath": 5.0,
        "LotArea": 14122.0,
        "CentralAir": "Y",
        "YearBuilt": 2005.0,
        "RemodAge": 5.0,
        "YearRemodAdd": 2006.0,
        "1stFlrSF": 1822.0,
        "HouseAge": 5.0,
        "GarageArea": 678.0,
        "GarageScore": 2034.0,
        "BsmtFinSF1": 28.0,
        "SaleCondition": "Normal",
        "TotalPorchSF": 119.0,
        "GarageCars": 3.0,
        "2ndFlrSF": 0.0,
        "Fireplaces": 1.0,
        "RoomsPlusBathEq": 11.5
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/clients/{client_id}/preferences/specific",
            json=json_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 3: Mixed data (both direct fields and JSON fields)
    print("=== Test 3: Mixed data ===")
    mixed_data = {
        # Direct preference fields
        "preferred_neighborhood": "NridgHt",
        "min_sale_price": 250000.0,
        "max_sale_price": 350000.0,
        # JSON fields that will be mapped
        "Neighborhood": "NridgHt",
        "YearBuilt": 2005.0,
        "LotArea": 14122.0,
        "GrLivArea": 1822.0,
        "Fireplaces": 1.0,
        "GarageCars": 3.0,
        "GarageArea": 678.0,
        "SaleCondition": "Normal"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/clients/{client_id}/preferences/specific",
            json=mixed_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Testing Specific Preferences Route")
    print("="*50)
    test_specific_preferences()
