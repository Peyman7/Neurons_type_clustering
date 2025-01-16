import numpy as np
import matplotlib.pyplot as plt

def calculate_isi_histogram(spikes, bins, plot=False):
    """
    Calculate the histogram of inter-spike intervals (ISI) for a specific neuron.

    Parameters:
        spikes (list of float): Spike timestamps in milliseconds.
        bins (np.array): Bin edges for the histogram.
        plot (bool): If True, plots the histogram of log(ISI).

    Returns:
        tuple:
            - isi_hist (np.array): Number of spikes in each bin.
            - bin_centers (np.array): Centers of the bins.
            - mode_isi (float): Bin center with the maximum number of spikes.
    """
    # Calculate ISI and log(ISI)
    isi = np.diff(spikes)
    isi_log = np.log10(isi)

    # Calculate histogram
    isi_hist, bin_edges = np.histogram(isi_log, bins=bins)
    bin_edges = 10 ** bin_edges
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

    if plot:
        # Plot histogram of log(ISI)
        plot_isi_histogram(bin_centers, isi_hist)

    # Determine mode ISI
    max_isi_idx = np.argmax(isi_hist)
    mode_isi = bin_centers[max_isi_idx]

    return isi_hist, bin_centers, mode_isi

def plot_isi_histogram(bin_centers, isi_hist):
    """Plot the histogram of log(ISI)."""
    plt.figure(figsize=(6, 4))
    plt.plot(bin_centers, isi_hist, '-', linewidth=0.8, color='blue')
    plt.xscale('log')
    plt.xlim([0.5, 10 ** 6])
    plt.ylim([0, max(isi_hist) + 50])
    plt.xlabel('Time (ms)')
    plt.ylabel('Number of Spikes')
    plt.title('Histogram of Log(ISI)')
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.show()

def main():
    """Main function to calculate ISI histogram for a specific neuron."""
    # Example inputs
    spikes = [0.1, 0.5, 1.2, 1.9, 3.0, 4.1]  # Spike timestamps in ms
    bins = np.arange(0, 10, 0.1)  # Bin edges for log(ISI)
    plot = True

    # Calculate ISI histogram
    isi_hist, bin_centers, mode_isi = calculate_isi_histogram(spikes, bins, plot)

    # Print results
    print("ISI Histogram:", isi_hist)
    print("Bin Centers:", bin_centers)
    print("Mode ISI:", mode_isi)

if __name__ == "__main__":
    main()
