# -*- coding: utf-8 -*-
"""
Created on Sat Aug 20 16:23:26 2022

@author: p.nazarirobati
"""
import os
import pandas as pd

def load_cluster_info(file_path):
    """Load the cluster information from a CSV file."""
    return pd.read_csv(file_path)

def process_spike_files(files_path, cluster_info_df):
    """
    Process spike train files to assign cell IDs based on the number of spikes.

    Parameters:
        files_path (str): Path to the directory containing spike train files.
        cluster_info_df (pd.DataFrame): DataFrame containing cluster information.

    Returns:
        pd.DataFrame: Updated cluster information DataFrame.
    """
    cell_counter = 0

    for root, _, files in os.walk(files_path):
        for file in sorted(files):
            if file.startswith('cell'):
                print(f"Processing file: {file}")

                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        data = f.read().split()

                    n_spikes = len(data)

                    # Locate the corresponding cluster entry
                    idx = cluster_info_df[cluster_info_df['Spikes'] == n_spikes].index.values
                    if len(idx) > 0:
                        cluster_info_df.loc[idx, 'cell'] = cell_counter + 1

                except Exception as e:
                    print(f"Error processing file {file}: {e}")

                cell_counter += 1

    return cluster_info_df

def save_cluster_info(cluster_info_df, output_path):
    """Save the updated cluster information to a CSV file."""
    try:
        cluster_info_df.to_csv(output_path, index=False)
        print(f"Updated cluster information saved to {output_path}")
    except Exception as e:
        print(f"Error saving updated cluster information: {e}")

def main():
    """Main function to process spike files and update cluster information."""
    # Define file paths
    SPIKES_FILE_PATH = r"C:\Users\p.nazarirobati\Desktop\spikes"
    CLUSTER_FILE_PATH = r"C:\Users\p.nazarirobati\Desktop\Cluster Sheet Features\rr5\rr5_2015-04-14_Cluster sheet_new.csv"
    OUTPUT_FILE_PATH = r"C:\Users\p.nazarirobati\Desktop\Cluster Sheet Features\rr5\rr5_2015-04-14_Cluster sheet_new.csv"

    # Load cluster information
    cluster_info_df = load_cluster_info(CLUSTER_FILE_PATH)

    # Process spike files
    updated_cluster_info = process_spike_files(SPIKES_FILE_PATH, cluster_info_df)

    # Save updated cluster information
    save_cluster_info(updated_cluster_info, OUTPUT_FILE_PATH)

if __name__ == "__main__":
    main()