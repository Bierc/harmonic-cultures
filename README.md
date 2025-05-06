# TimbreSpace

A cross-cultural exploration of musical timbre using spectral analysis and dimensionality reduction techniques.  
This project maps and visualizes how songs from different regions relate in timbre space.

## 🎯 Objective

To investigate whether music from different countries or cultures forms distinct clusters in a computational timbre space, and whether acoustic similarity reflects cultural or stylistic proximity.

## ⚙️ Technologies Used

- Python 3
- Librosa
- NumPy / Pandas
- Scikit-learn
- Plotly / Seaborn
- UMAP / t-SNE / PCA

## 📊 Dataset Overview

This project uses a custom-curated dataset of **120 songs** from **6 different regions**, each representing a variety of musical cultures through distinct genres and artists.

### 🌍 Countries and Styles

The dataset includes **4 musical styles per country**, with **5 representative songs** per style:

| Country         | Styles                                           | Tracks |
|------------------|--------------------------------------------------|--------|
| **Brazil**       | Samba, Bossa Nova, Funk Carioca, Chorinho       | 20     |
| **India**        | Bollywood, Classical, Bhajan, Folk              | 20     |
| **Japan**        | City Pop, J-Pop, Min’yō, Enka                   | 20     |
| **USA**          | Blues, Jazz, Soul, Folk                         | 20     |
| **West Africa**  | Afrobeat, Highlife, Juju, Mbalax                | 20     |
| **Middle East**  | Maqam, Dabke, Arabic Pop, Traditional           | 20     |

**Total:** `120 tracks`, covering `24 genres` from traditional, classical, and folk to modern pop and soul.

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

### 🧩 Purpose

This dataset serves as the foundation for building **timbre-based representations of music**, allowing analysis of acoustic similarity across styles, countries, and cultural backgrounds. It supports experiments in clustering, dimensionality reduction, and timbre space visualization.


## Project Structure

```
├── data/ # Raw and processed audio data 
├── notebooks/ # Jupyter notebooks for analysis and visualization 
├── scripts/ # Python scripts for preprocessing and feature extraction 
├── results/ # Outputs like plots, embeddings, and metrics 
└── README.md
```
## 🔍 Methods

1. Feature extraction using mel spectrograms and low-level spectral descriptors.
2. Vector representation of each audio track using statistical aggregation.
3. Dimensionality reduction to project high-dimensional timbre features into 2D.
4. Visualization and analysis of clusters by region, style, and cultural influence.

## 📌 Status

Project under active development — data collection and initial feature extraction in progress.
