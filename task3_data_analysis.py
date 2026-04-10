import pandas as pd
import numpy as np
import os

def analyze_trends():
    # Step 1: Load and Explore
    file_path = 'data/trends_clean.csv'
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found. Please run Task 2 first.")
        return

    df = pd.read_csv(file_path)
    
    print(f"Loaded data: {df.shape}")
    print("\nFirst 5 rows:")
    print(df.head())
    
    # Calculate global averages using Pandas
    avg_score = df['score'].mean()
    avg_comments = df['num_comments'].mean()
    
    print(f"\nAverage score   : {avg_score:,.2f}")
    print(f"Average comments: {avg_comments:,.2f}")

    # Step 2: Basic Analysis with NumPy
    print("\n--- NumPy Stats ---")
    
    # Convert columns to NumPy arrays for calculations
    scores = df['score'].to_numpy()
    comments = df['num_comments'].to_numpy()
    
    print(f"Mean score   : {np.mean(scores):,.2f}")
    print(f"Median score : {np.median(scores):,.2f}")
    print(f"Std deviation: {np.std(scores):,.2f}")
    print(f"Max score    : {np.max(scores)}")
    print(f"Min score    : {np.min(scores)}")

    # Find category with most stories
    most_popular_cat = df['category'].value_counts().idxmax()
    cat_count = df['category'].value_counts().max()
    print(f"\nMost stories in: {most_popular_cat} ({cat_count} stories)")

    # Find story with most comments using NumPy index
    max_comments_idx = np.argmax(comments)
    top_story_title = df.iloc[max_comments_idx]['title']
    top_story_comments = df.iloc[max_comments_idx]['num_comments']
    print(f"Most commented story: \"{top_story_title}\" — {top_story_comments} comments")

    # Step 3: Add New Columns
    # engagement = num_comments / (score + 1) to avoid division by zero
    df['engagement'] = df['num_comments'] / (df['score'] + 1)
    
    # is_popular = True if score is above the dataset average
    df['is_popular'] = df['score'] > avg_score

    # Step 4: Save the Result
    output_file = 'data/trends_analysed.csv'
    df.to_csv(output_file, index=False)
    print(f"\nSaved to {output_file}")

if __name__ == "__main__":
    analyze_trends()

