import pandas as pd
import seaborn as sns
import argparse
import matplotlib.pyplot as plt

def graph_n_effects_samefig(data, x_column):
    """
    Graphs the effect of one column on multiple other columns using Seaborn.
    
    Parameters:
        data (DataFrame): The pandas DataFrame containing the data.
        x_column (str): The column to be plotted on the x-axis.
    """
    fig, ax1 = plt.subplots(figsize=(10, 10))
    tidy = data.melt(id_vars=x_column).rename(columns=str.title)
    sns.barplot(x=x_column, y='Value', hue='Variable', data=tidy, ax=ax1)
    plt.xlabel(x_column)
    plt.xticks(rotation=45, ha='right') 
    sns.despine(fig)
    filename = f"effect_of_{x_column.lower().replace(' ', '_')}.png"
    plt.savefig(filename)
    print(f"Graph saved as {filename}")

def graph_n_effects(data, x_column, *y_columns):
    """
    Graphs the effect of one column on multiple other columns using Seaborn.
    
    Parameters:
        data (DataFrame): The pandas DataFrame containing the data.
        x_column (str): The column to be plotted on the x-axis.
        *y_columns (str): The columns to be plotted on the y-axis.
    """
    data = data.sort_values(by=[x_column], ascending=True)
    num_plots = len(y_columns)
    plt.figure(figsize=(5 * num_plots, 6))
    
    for i, y_column in enumerate(y_columns):
        plt.subplot(1, num_plots, i+1)
        sns.barplot(x=x_column, y=y_column, data=data)
        plt.title(f'Effect of {x_column} on {y_column}')
        plt.xlabel(x_column)
        plt.xticks(rotation=45, ha='right') 
        plt.ylabel(y_column)
    
    plt.tight_layout()
    filename = f"effect_of_{x_column.lower().replace(' ', '_')}_on_{'_and_'.join([y.lower().replace(' ', '_') for y in y_columns])}.png"
    plt.savefig(filename)
    print(f"Graph saved as {filename}")


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

def analyze_effects(csv_file, args):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    factor = df.columns[args.factor]
    
    # Create a barplot to visualize the average execution time for each combination of Scene, Sampler, and Integrator
    if args.same:
        graph_n_effects_samefig(df, factor)
    else:
        if len(args.variables) == 2:
            graph_two_effects(df, df.columns[args.variables[0]], df.columns[args.variables[1]], df.columns[args.variables[2]])
        else:
            graph_n_effects(df, factor, [df.columns[i] for i in args.variables])
    
    print("done")

def main():
    # Specify the path to the CSV file
    parser = argparse.ArgumentParser(description='Process CSV file.')
    parser.add_argument('csv_file', type=str, help='Path to the CSV file')
    parser.add_argument('--factor', type=int, default=0, help='Column of the factor variable', nargs='?')
    parser.add_argument('--variables', '--var', type=int, nargs='+', default=[1, 2], help='Columns of the variables')
    parser.add_argument('--same', type=bool, default=True, help='Flag to indicate whether to plot all effects in the same figure')

    args = parser.parse_args()
    csv_file = args.csv_file

    # Call the analyze_effects function with the CSV file path
    analyze_effects(csv_file, args)

if __name__ == "__main__":
    main()
