import os
import numpy as np
import pandas as pd
from ISI_Histogram import ISI_Histogram
from CrossCorrelation_Histogram import CrossCorrelation_Histogram

def load_cluster_info(file_path):
    """Load the cluster information from a CSV file."""
    return pd.read_csv(file_path)

def process_spike_file(file_path, t_start, t_end, isi_bins, bin_size, lag):
    """Process a single spike file to calculate ISI and cross-correlation histograms."""
    try:
        with open(file_path, 'r') as f:
            data = f.read().split()
        spike_times = [int(val) / 1000 for val in data]  # Convert to ms

        # ISI Histogram
        isi_hist, bin_centers, mode_isi = ISI_Histogram(spike_times, isi_bins, plot=False)

        # Auto-correlation Histogram
        spike_times_ac = [int(val) / 100 for val in data]  # Convert to 0.1 ms
        spike_times_ac = [t for t in spike_times_ac if t_start <= t <= t_end]

        cross_corr_lag, peak_cch, median_cch = CrossCorrelation_Histogram(
            spike_times_ac, spike_times_ac, bin_size, t_start, t_end, lag, plot=False
        )

        return mode_isi, peak_cch + 1, median_cch + 1

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None, None, None

def update_cluster_info(cluster_info_df, cell_id, mode_isi, peak_cch, median_cch):
    """Update the cluster info DataFrame with calculated metrics."""
    idx = cluster_info_df[cluster_info_df['cell'] == cell_id].index.values
    if len(idx) == 0:
        print(f"Warning: Cell {cell_id} not found in cluster sheet.")
        return

    cluster_info_df.loc[idx, 'Mode_ISI'] = mode_isi
    cluster_info_df.loc[idx, 'AC_peak'] = peak_cch
    cluster_info_df.loc[idx, 'AC_median'] = median_cch

def save_cluster_info(cluster_info_df, output_path):
    """Save the updated cluster information to a CSV file."""
    try:
        cluster_info_df.to_csv(output_path, index=False)
        print(f"Results saved to {output_path}")
    except Exception as e:
        print(f"Error saving results: {e}")

def main():
    # Define file paths
    SPIKES_FILE_PATH = r"C:\Users\p.nazarirobati\Desktop\spikes"
    CLUSTER_FILE_PATH = r"C:\Users\p.nazarirobati\Desktop\Cluster Sheet Features\rr5\rr5_2015-04-14_Cluster sheet_new.csv"
    RESULT_FILE_PATH = r"C:\Users\p.nazarirobati\Desktop\Cluster Sheet Features\rr5\rr5_2015-04-14_Cluster sheet_new.csv"

    # Load cluster sheet DataFrame
    cluster_info_df = load_cluster_info(CLUSTER_FILE_PATH)

    # Time parameters in 0.1 ms scale
    t_start = 79125275.19
    t_end = 318814904.85

    # ISI Histogram parameters
    isi_bins = np.arange(0, 10, 0.011)  # Bin size in ms

    # Cross-correlation parameters
    bin_size = 10  # Bin size in 0.1 ms
    lag = 50  # Lag in 0.1 ms

    # Process each spike train file
    cell_counter = 1
    for root, _, files in os.walk(SPIKES_FILE_PATH):
        for file in sorted(files):
            if file.startswith('cell'):
                print(f"Processing file: {file}")

                file_path = os.path.join(root, file)
                mode_isi, peak_cch, median_cch = process_spike_file(
                    file_path, t_start, t_end, isi_bins, bin_size, lag
                )

                if mode_isi is not None:
                    update_cluster_info(cluster_info_df, cell_counter, mode_isi, peak_cch, median_cch)

                cell_counter += 1

    # Save updated cluster sheet
    save_cluster_info(cluster_info_df, RESULT_FILE_PATH)

if __name__ == "__main__":
    main()
