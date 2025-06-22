# TimbreSpace

A cross-cultural exploration of musical timbre using spectral analysis and dimensionality reduction techniques.  
This project maps and visualizes how songs from different regions relate in timbre space.

## Objective

To investigate whether music from different countries or cultures forms distinct clusters in a computational timbre space, and whether acoustic similarity reflects cultural or stylistic proximity.

## Technologies Used

- Python 3
- Librosa
- NumPy / Pandas
- Scikit-learn
- Plotly / Seaborn
- UMAP / t-SNE / PCA

## Dataset Overview

This project uses a custom-curated dataset of **120 songs** from **6 different regions**, each representing a variety of musical cultures through distinct genres and artists.

### Countries and Styles

We manually curated a dataset of **90 songs** from **3 stylistically similar genres**:

| Style     | Country        | Tracks |
|-----------|----------------|--------|
| Samba     | Brazil         | 30     |
| Jazz      | USA            | 30     |
| Afrobeat  | West Africa    | 30     |

### 🗂 Dataset Columns

| Column        | Description                                                    |
|---------------|----------------------------------------------------------------|
| `id`          | Unique identifier for each song                                |
| `country`     | Country or region of origin                                    |
| `style`       | Musical genre or substyle                                      |
| `artist`      | Performing artist or group                                     |
| `track_title` | Title of the track                                             |
| `link`        | YouTube or audio source (to be filled manually)                |
| `source`      | Platform or origin of the song data (default: YouTube)         |
| `license`     | Assumed license (default: Fair use; can be adjusted if needed) |
| `notes`       | Additional comments (optional)                                 |

### Purpose

This dataset serves as the foundation for building **timbre-based representations of music**, allowing analysis of acoustic similarity across styles, countries, and cultural backgrounds. It supports experiments in clustering, dimensionality reduction, and timbre space visualization.


## Project Structure

```
├── data/ # Raw and processed audio data 
├── notebooks/ # Jupyter notebooks for analysis and visualization 
├── scripts/ # Python scripts for preprocessing and feature extraction 
├── results/ # Outputs like plots, embeddings, and metrics 
└── README.md
```
### Feature Extraction

We extracted a total of **74 features** per song, including:

- **Global descriptors:** MFCCs, spectral centroid, roll-off, and bandwidth  
- **Harmonic features:** Chroma and tonnetz descriptors (from HPSS harmonic component)  
- **Percussive features:** ZCR, spectral flatness, and RMS energy (from HPSS percussive component)

All features were aggregated using mean and standard deviation.


## Methods

1. **Feature Extraction:** Using Librosa + HPSS separation to isolate harmonic/percussive content.
2. **Normalization:** Z-score standardization for all feature vectors.
3. **Dimensionality Reduction:** PCA, t-SNE, and UMAP for projecting features into 2D space.
4. **Clustering:** KMeans and HDBSCAN were used to detect structure within the projected space.
5. **Evaluation:** Clusters and embeddings were evaluated using Silhouette Score, Calinski-Harabasz, and Davies-Bouldin indices.
6. **Qualitative Analysis:** Observational analysis was conducted to compare the projections with perceptual expectations.

