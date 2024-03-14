import pandas as pd
import seaborn as sns
import argparse
import matplotlib.pyplot as plt

# Function to generate a barplot to visualize the variable for each combination of two columns
def generate_barplot(df, x_column, y_column, hue_column, title):    
    df = df.sort_values(by=[x_column], ascending=True)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=x_column, y=y_column, hue=hue_column, data=df, errorbar=None)
    plt.title(title)
    plt.xlabel(x_column)
    plt.ylim(0, df[y_column].max())
    plt.xticks(rotation=45, ha='right')
    df = df.sort_values(by=[x_column], ascending=False)
    plt.ylabel(y_column)
    plt.xticks(rotation=45)
    plt.legend(title=hue_column)
    plt.tight_layout()
    plt.savefig(f"effect_of_{x_column.lower().replace(' ', '_')}_and_{hue_column.lower().replace(' ', '_')}.png")

def analyze_effects(csv_file):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Analyze the effects of the first three columns on the last column
    fourth_column_name = df.columns[3]

    # Create a barplot to visualize the average execution time for each combination of Scene, Sampler, and Integrator
    generate_barplot(df, "Scene", fourth_column_name, "Sampler", "Effect of Scene and Sampler on " + fourth_column_name)

    # Create a barplot to visualize the average execution time for each combination of Scene, Sampler, and Integrator
    generate_barplot(df, "Scene", fourth_column_name, "Integrator", "Effect of Scene and Integrator on " + fourth_column_name)

    print("done")

def main():
    # Specify the path to the CSV file
    parser = argparse.ArgumentParser(description='Process CSV file.')
    parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    args = parser.parse_args()

    csv_file = args.csv_file

    # Call the analyze_effects function with the CSV file path
    analyze_effects(csv_file)

if __name__ == "__main__":
    main()
