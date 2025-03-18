import pandas as pd
from prefect import flow, task

# ✅ Update the correct column name
COLUMN_NAME = "Payload Mass (kg)"
FILE_PATH = r"D:\NASA_Meteorite_Dashboard\spacex_launch_data_fixed.csv"

@task
def extract():
    """Extract data from the CSV file"""
    try:
        df = pd.read_csv(FILE_PATH)
        print("✅ Data loaded successfully.")
        print("📊 Columns in dataset:", df.columns)
        return df
    except FileNotFoundError:
        print(f"🚨 Error: File not found at {FILE_PATH}")
        return None

@task
def transform(df):
    """Transform data - Handle missing payload mass values"""
    if df is not None:
        if COLUMN_NAME not in df.columns:
            print(f"🚨 Error: Column '{COLUMN_NAME}' not found in dataset!")
            return None
        
        # ✅ Convert to numeric, fill missing values with 0
        df[COLUMN_NAME] = pd.to_numeric(df[COLUMN_NAME], errors="coerce").fillna(0)
        
        print(f"✅ Data transformation complete. {len(df)} rows remaining.")
        return df
    return None

@task
def load(df):
    """Load the transformed data into a new CSV file"""
    if df is not None:
        output_path = r"D:\NASA_Meteorite_Dashboard\spacex_launch_transformed.csv"
        df.to_csv(output_path, index=False)
        print(f"✅ Transformed data saved to {output_path}")

@flow
def etl_pipeline():
    """Main ETL Flow"""
    df = extract()
    df = transform(df)
    load(df)

# Run the pipeline
if __name__ == "__main__":
    etl_pipeline()
