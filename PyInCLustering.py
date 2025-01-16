# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 22:08:16 2022

@author: p.nazarirobati (p.nazarirobati@uleth.ca)
### This is a script for clsutering pyramidal/ interneuron cells
"""
import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score

# Functions

def load_cluster_data(file_path_pattern):
    """Load and preprocess clustering data from multiple CSV files."""
    df = pd.concat(map(pd.read_csv, glob.glob(file_path_pattern)))
    df = df.drop(['Strange', 'ISI_Biom'], axis=1, errors='ignore')
    df = df.dropna()
    df['Mode_ISI'] = df['Mode_ISI'].astype(float)
    return df

def plot_features(df):
    """Plot scatter plots of selected features."""
    fig, ax = plt.subplots(2, 3, figsize=(10, 6))

    features = [
        ('pk-tr width', 'Firing Rate'),
        ('halfpeak width', 'Firing Rate'),
        ('Mode_ISI', 'Firing Rate'),
        ('AC_peak', 'Firing Rate'),
        ('AC_median', 'Firing Rate'),
        ('AC_median - AC_peak', 'Firing Rate')
    ]

    for i, (x, y) in enumerate(features):
        row, col = divmod(i, 3)
        if x in df.columns and y in df.columns:
            ax[row, col].scatter(df[x], df[y], s=4)
            ax[row, col].set_xlabel(x, fontweight='bold')
            ax[row, col].set_ylabel(y, fontweight='bold')

    fig.suptitle('Feature Scatter Plots', fontweight='bold')
    plt.show()

def reduce_dimensionality(data, method='pca', n_components=2):
    """Perform dimensionality reduction."""
    if method == 'pca':
        reducer = PCA(n_components=n_components)
    elif method == 'tsne':
        from sklearn.manifold import TSNE
        reducer = TSNE(n_components=n_components)
    elif method == 'umap':
        import umap
        reducer = umap.UMAP(n_components=n_components, random_state=42)
    else:
        raise ValueError("Unsupported reduction method")

    reduced_data = reducer.fit_transform(data)
    return reduced_data

def perform_clustering(data, method='kmeans', n_clusters=2):
    """Cluster the data using the specified method."""
    if method == 'kmeans':
        model = KMeans(n_clusters=n_clusters, random_state=42)
    elif method == 'dbscan':
        model = DBSCAN(eps=0.95, min_samples=5)
    else:
        raise ValueError("Unsupported clustering method")

    labels = model.fit_predict(data)
    silhouette_avg = silhouette_score(data, labels) if len(np.unique(labels)) > 1 else None
    return labels, silhouette_avg

def plot_clustering_results(data, labels):
    """Plot clustering results in 2D."""
    unique_labels = np.unique(labels)
    colors = plt.cm.get_cmap('tab10', len(unique_labels))

    fig, ax = plt.subplots()
    for label in unique_labels:
        ax.scatter(
            data[labels == label, 0],
            data[labels == label, 1],
            s=5,
            label=f'Cluster {label}',
            color=colors(label)
        )

    ax.set_xlabel('Dim1')
    ax.set_ylabel('Dim2')
    ax.legend()
    plt.title('Clustering Results')
    plt.show()

def main():
    # Load data
    file_path_pattern = r"C:\Users\p.nazarirobati\Desktop\Cluster Sheet Features\Modified\*.csv"
    df = load_cluster_data(file_path_pattern)

    # Plot feature scatter plots
    plot_features(df)

    # Select features for clustering
    selected_features = ['pk-tr width', 'Firing Rate', 'Mode_ISI', 'AC_peak']
    df_selected = df[selected_features].dropna()
    df_normalized = StandardScaler().fit_transform(df_selected)

    # Dimensionality reduction
    reduced_data = reduce_dimensionality(df_normalized, method='pca', n_components=2)

    # Perform clustering
    labels, silhouette_avg = perform_clustering(reduced_data, method='kmeans', n_clusters=2)
    print(f"Silhouette Score: {silhouette_avg}")

    # Plot clustering results
    plot_clustering_results(reduced_data, labels)

if __name__ == "__main__":
    main()
