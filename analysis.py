import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def analyze_effects(csv_file):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Analyze the effects of the first three columns on the last column
    fourth_column_name = df.columns[3]
    plt.figure(figsize=(12, 6))

    # Create a barplot to visualize the average execution time for each combination of Scene, Sampler, and Integrator
    sns.barplot(x="Scene", y=fourth_column_name, hue="Sampler", data=df, errorbar=None)
    plt.title("Effect of Scene and Sampler on " + fourth_column_name)
    plt.xlabel("Scene")
    plt.xticks(rotation=45, ha='right')
    plt.gca().set_xticklabels(sorted(df['Scene'].unique()))
    plt.ylabel(fourth_column_name)
    plt.xticks(rotation=45)
    plt.legend(title="Sampler")
    plt.tight_layout()

    # Save the plot to a file or display it
    plt.savefig("effect_of_scene_and_sampler.png")

    # Analyze the effects of the first three columns on the last column
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6))

    # Create a barplot to visualize the average execution time for each combination of Scene, Sampler, and Integrator
    sns.barplot(x="Scene", y=fourth_column_name, hue="Integrator", data=df, errorbar=None)
    plt.title("Effect of Scene and Integrator on " + fourth_column_name)
    plt.xlabel("Scene")
    plt.xticks(rotation=45, ha='right')
    plt.gca().set_xticklabels(sorted(df['Scene'].unique()))
    plt.ylabel(fourth_column_name)
    plt.xticks(rotation=45)
    plt.legend(title="Integrator")
    plt.tight_layout()

    # Save the plot to a file or display it
    plt.savefig("effect_of_scene_and_integrator.png")
    print("done")


def main():
    # Specify the path to the CSV file
    csv_file = "./output.csv"

    # Call the analyze_effects function with the CSV file path
    analyze_effects(csv_file)

if __name__ == "__main__":
    main()
