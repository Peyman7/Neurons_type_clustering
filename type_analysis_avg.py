import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_and_process_rat_data(rats, base_path):
    """
    Load and process pyramidal, interneuron, and unclassified neuron data for multiple rats.

    Parameters:
        rats (list): List of rat identifiers.
        base_path (str): Base path to the data files.

    Returns:
        tuple:
            - PyrInt_all (pd.DataFrame): Combined data for all rats.
            - PyrInt_avg (pd.DataFrame): Average data per rat.
    """
    PyrInt_all = pd.DataFrame(columns=['Rat', 'Pyramidal', 'Interneuron', 'Unclassified'])
    PyrInt_avg = pd.DataFrame(columns=['Rat', 'Pyramidal', 'Interneuron', 'Unclassified'])

    for ind, rat in enumerate(rats):
        filepath = os.path.join(base_path, f"{rat}_PyramidalInterneurons_len.csv")
        PyrInt = pd.read_csv(filepath, sep=',')

        # Normalize percentages
        PyrInt['Pyramidal'] = 100 * PyrInt['Pyramidal'] / PyrInt['nneu']
        PyrInt['Interneuron'] = 100 * PyrInt['Interneuron'] / PyrInt['nneu']
        PyrInt['Unclassified'] = 100 * PyrInt['Unclassified'] / PyrInt['nneu']

        # Combine data
        PyrInt_all = pd.concat([PyrInt_all, PyrInt], axis=0)

        # Calculate averages
        PyrInt_avg.loc[ind, 'Rat'] = f"Rat {ind + 1}"
        PyrInt_avg.loc[ind, 'Pyramidal'] = PyrInt['Pyramidal'].mean()
        PyrInt_avg.loc[ind, 'Interneuron'] = PyrInt['Interneuron'].mean()
        PyrInt_avg.loc[ind, 'Unclassified'] = PyrInt['Unclassified'].mean()

    return PyrInt_all, PyrInt_avg

def plot_average_neurons_percentage(PyrInt_avg):
    """
    Plot the average neuron percentage per day for pyramidal, interneuron, and unclassified neurons.

    Parameters:
        PyrInt_avg (pd.DataFrame): DataFrame with average data per rat.
    """
    df = pd.melt(PyrInt_avg, id_vars="Rat", var_name="Type", value_name="Average Neurons Percentage/day")
    sns.catplot(x='Rat', y='Average Neurons Percentage/day', hue='Type', data=df, kind='bar')
    plt.title("Average Neurons Percentage Per Day by Rat")
    plt.show()

def plot_neuron_distribution(PyrInt_all):
    """
    Plot histograms for the distribution of pyramidal, interneuron, and unclassified neurons.

    Parameters:
        PyrInt_all (pd.DataFrame): Combined data for all rats.
    """
    fig, ax = plt.subplots(1, 3, figsize=(12, 6))

    sns.histplot(PyrInt_all['Pyramidal'], stat='percent', ax=ax[0])
    ax[0].set_title('Pyramidal Neurons')
    ax[0].set_xlabel('Percentage')

    sns.histplot(PyrInt_all['Interneuron'], stat='percent', ax=ax[1])
    ax[1].set_title('Interneuron Neurons')
    ax[1].set_xlabel('Percentage')

    sns.histplot(PyrInt_all['Unclassified'], stat='percent', ax=ax[2])
    ax[2].set_title('Unclassified Neurons')
    ax[2].set_xlabel('Percentage')

    plt.tight_layout()
    plt.show()

def main():
    # Define parameters
    rats = ['rr5', 'rr6', 'rr7', 'rr8', 'rr9']
    base_path = r"C:\Users\p.nazarirobati\Desktop\Analysis\Pyramidal vs Interneurons\Method 1\len"

    # Load and process data
    PyrInt_all, PyrInt_avg = load_and_process_rat_data(rats, base_path)

    # Plot results
    plot_average_neurons_percentage(PyrInt_avg)
    plot_neuron_distribution(PyrInt_all)

if __name__ == "__main__":
    main()
