import pandas as pd

print("Starting ML Training Script...")

# Load the dataset
try:
    data = pd.read_csv('travel_data.csv')
    print(f"Dataset loaded successfully!")
    print(f"Dataset shape: {data.shape}")
    print("\nFirst 5 rows:")
    print(data.head())
    
    # Simple validation
    print("\n=== QUICK VALIDATION ===")
    print(f"Columns: {list(data.columns)}")
    print(f"Total rows: {len(data)}")
    print(f"Sample recommended_items: {data['recommended_items'].head().tolist()}")
    
    print("\nScript completed successfully!")
    
except FileNotFoundError:
    print("ERROR: travel_data.csv not found!")
    print("Please ensure travel_data.csv is in the same folder as this script.")
except Exception as e:
    print(f"ERROR: {e}")

input("Press Enter to exit...")