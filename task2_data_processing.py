import pandas as pd
import glob
import os

def process_trend_data():
    # Step 1: Load the JSON File
    # We look for the most recent trends JSON file in the data folder
    json_files = glob.glob('data/trends_*.json')
    if not json_files:
        print("Error: No JSON data files found in data/ folder.")
        return

    # Sort files to get the most recent one if multiple exist
    latest_file = sorted(json_files)[-1]
    
    df = pd.read_json(latest_file)
    print(f"Loaded {len(df)} stories from {latest_file}")

    # Step 2: Clean the Data
    
    # 1. Duplicates: Remove rows with the same post_id
    df = df.drop_duplicates(subset=['post_id'])
    print(f"After removing duplicates: {len(df)}")

    # 2. Missing values: Drop rows missing critical fields
    df = df.dropna(subset=['post_id', 'title', 'score'])
    print(f"After removing nulls: {len(df)}")

    # 3. Low quality: Remove stories where score is less than 5
    df = df[df['score'] >= 5]
    print(f"After removing low scores: {len(df)}")

    # 4. Data types: Ensure score and num_comments are integers
    df['score'] = df['score'].astype(int)
    df['num_comments'] = df['num_comments'].astype(int)

    # 5. Whitespace: Strip extra spaces from the title column
    df['title'] = df['title'].str.strip()

    # Step 3: Save as CSV
    output_path = 'data/trends_clean.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\nSaved {len(df)} rows to {output_path}")

    # Print summary of stories per category
    print("\nStories per category:")
    category_summary = df['category'].value_counts()
    for category, count in category_summary.items():
        print(f"  {category:<15} {count}")

if __name__ == "__main__":
    process_trend_data()

