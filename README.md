# Neural Cell Clustering: Pyramidal and Interneuron Analysis

This repository contains Python scripts for analyzing and clustering neural cells into pyramidal, interneuron, and unclassified categories. The analysis involves data preprocessing, visualization, and clustering using various machine learning techniques. Below is an overview of the included functionality and usage.

## Features

### 1. **Data Loading and Preprocessing**
   - Load neural cell data for multiple rats from CSV files.
   - Normalize neuron percentages by dividing neuron counts by the total number of neurons in each dataset.
   - Compute average percentages for each neuron type (pyramidal, interneuron, unclassified) per rat.

### 2. **Data Visualization**
   - **Scatter Plots**:
     Visualize relationships between key features, such as firing rates, peak-trough widths, and ISI values.
   - **Bar Charts**:
     Show average neuron percentages per day for pyramidal, interneuron, and unclassified neurons across rats.
   - **Histograms**:
     Display the distribution of neuron types across all rats.

### 3. **Dimensionality Reduction and Clustering**
   - Perform dimensionality reduction using PCA, UMAP, or t-SNE.
   - Apply clustering algorithms such as K-Means or DBSCAN to categorize neurons based on their properties.
   - Evaluate clustering results using silhouette scores.
