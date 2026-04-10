import pandas as pd
import matplotlib.pyplot as plt
import os

def create_visualizations():
    # 1. Setup
    file_path = 'data/trends_analysed.csv'
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found. Please run Task 3 first.")
        return

    df = pd.read_csv(file_path)
    
    # Create outputs folder if it doesn't exist
    if not os.path.exists('outputs'):
        os.makedirs('outputs')

    # 2. Chart 1: Top 10 Stories by Score
    plt.figure(figsize=(10, 6))
    top_10 = df.nlargest(10, 'score').copy()
    # Shorten titles longer than 50 characters
    top_10['short_title'] = top_10['title'].apply(lambda x: x[:47] + '...' if len(x) > 50 else x)
    
    plt.barh(top_10['short_title'], top_10['score'], color='skyblue')
    plt.xlabel('Score')
    plt.title('Top 10 Stories by Score')
    plt.gca().invert_yaxis()  # Highest score at the top
    plt.tight_layout()
    plt.savefig('outputs/chart1_top_stories.png')
    plt.close()

    # 3. Chart 2: Stories per Category
    plt.figure(figsize=(10, 6))
    cat_counts = df['category'].value_counts()
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0']
    
    cat_counts.plot(kind='bar', color=colors[:len(cat_counts)])
    plt.title('Number of Stories per Category')
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('outputs/chart2_categories.png')
    plt.close()

    # 4. Chart 3: Score vs Comments
    plt.figure(figsize=(10, 6))
    popular = df[df['is_popular'] == True]
    not_popular = df[df['is_popular'] == False]
    
    plt.scatter(popular['score'], popular['num_comments'], color='orange', label='Popular', alpha=0.6)
    plt.scatter(not_popular['score'], not_popular['num_comments'], color='blue', label='Regular', alpha=0.6)
    
    plt.title('Score vs Number of Comments')
    plt.xlabel('Score')
    plt.ylabel('Comments')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('outputs/chart3_scatter.png')
    plt.close()

    # BONUS: Dashboard
    fig, axs = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('TrendPulse Dashboard', fontsize=20, fontweight='bold')

    # Re-plot Chart 1 on Dashboard
    axs[0, 0].barh(top_10['short_title'], top_10['score'], color='skyblue')
    axs[0, 0].set_title('Top 10 Stories')
    axs[0, 0].invert_yaxis()

    # Re-plot Chart 2 on Dashboard
    axs[0, 1].bar(cat_counts.index, cat_counts.values, color=colors[:len(cat_counts)])
    axs[0, 1].set_title('Stories per Category')
    axs[0, 1].tick_params(axis='x', rotation=45)

    # Re-plot Chart 3 on Dashboard
    axs[1, 0].scatter(popular['score'], popular['num_comments'], color='orange', label='Popular')
    axs[1, 0].scatter(not_popular['score'], not_popular['num_comments'], color='blue', label='Regular')
    axs[1, 0].set_title('Engagement: Score vs Comments')
    axs[1, 0].legend()

    # Summary Text in the 4th slot
    axs[1, 1].axis('off')
    summary_text = (
        f"Total Stories: {len(df)}\n"
        f"Avg Score: {df['score'].mean():.1f}\n"
        f"Avg Comments: {df['num_comments'].mean():.1f}\n"
        f"Most Popular Category: {cat_counts.idxmax()}"
    )
    axs[1, 1].text(0.5, 0.5, summary_text, fontsize=14, ha='center', va='center', 
                  bbox=dict(facecolor='white', alpha=0.5))

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('outputs/dashboard.png')
    plt.show()
    print("Visualizations complete. Files saved in outputs/ folder.")

if __name__ == "__main__":
    create_visualizations()

