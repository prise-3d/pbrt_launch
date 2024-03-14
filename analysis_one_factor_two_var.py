import pandas as pd
import seaborn as sns
import argparse
import matplotlib.pyplot as plt


def graph_two_effects(data, x_column, y_column1, y_column2):
    """
    Graphs the effect of one column on two other columns using Seaborn.
    
    Parameters:
        data (DataFrame): The pandas DataFrame containing the data.
        x_column (str): The column to be plotted on the x-axis.
        y_column1 (str): The first column to be plotted on the y-axis.
        y_column2 (str): The second column to be plotted on the y-axis.
    """
    data = data.sort_values(by=[x_column], ascending=True)
    plt.figure(figsize=(10, 6))
    
    # Plot for y_column1
    plt.subplot(1, 2, 1)
    sns.barplot(x=x_column, y=y_column1, data=data)
    plt.title(f'Effect of {x_column} on {y_column1}')
    plt.xlabel(x_column)
    plt.xticks(rotation=45, ha='right') 
    plt.ylabel(y_column1)
    
    # Plot for y_column2
    plt.subplot(1, 2, 2)
    sns.barplot(x=x_column, y=y_column2, data=data)
    plt.title(f'Effect of {x_column} on {y_column2}')
    plt.xlabel(x_column)
    plt.xticks(rotation=45, ha='right') 
    plt.ylabel(y_column2)
    
    plt.tight_layout()
    filename = f"effect_of_{x_column.lower().replace(' ', '_')}_on_{y_column1.lower().replace(' ', '_')}_and_{y_column1.lower().replace(' ', '_')}.png"
    plt.savefig(filename)
    print(f"Graph saved as {filename}")

def analyze_effects(csv_file):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    factor = df.columns[0]
    var1 = df.columns[1]
    var2 = df.columns[2]

    # Create a barplot to visualize the average execution time for each combination of Scene, Sampler, and Integrator
    graph_two_effects(df, factor, var1, var2)

    

    print("done")

def main():
    # Specify the path to the CSV file
    parser = argparse.ArgumentParser(description='Process CSV file.')
    parser.add_argument('csv_file', type=str, help='Path to the CSV file')
    parser.add_argument('--factor', type=int, default=0, help='Column of the factor variable', nargs='?')
    parser.add_argument('--var1', type=int, default=1, help='Column of first variable')
    parser.add_argument('--var2', type=int, default=2, help='Column of second variable')

    args = parser.parse_args()
    csv_file = args.csv_file

    # Call the analyze_effects function with the CSV file path
    analyze_effects(csv_file)

if __name__ == "__main__":
    main()
