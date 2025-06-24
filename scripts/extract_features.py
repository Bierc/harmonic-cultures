import os
import librosa
import numpy as np
import pandas as pd
from tqdm import tqdm

# directories
RAW_DIR = "data/raw_subsets"
OUTPUT_CSV = "data/features_audio_subset_new.csv"
DURATION = 200  # seconds

def extract_features_from_hpss(file_path, duration=200, sr=22050):
    try:
        y, sr = librosa.load(file_path, sr=sr)
        if len(y) > duration * sr:
            y = y[:duration * sr]

        # harmonic-percussive source separation
        y_harm, y_perc = librosa.effects.hpss(y)

        # global features
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)

        # harmonic features
        chroma = librosa.feature.chroma_stft(y=y_harm, sr=sr)
        tonnetz = librosa.feature.tonnetz(y=y_harm, sr=sr)

        # percussive features
        zcr = librosa.feature.zero_crossing_rate(y=y_perc)
        flatness = librosa.feature.spectral_flatness(y=y_perc)
        rms = librosa.feature.rms(y=y_perc)

        features = {
            "filename": os.path.basename(file_path),
            "style": os.path.basename(os.path.dirname(file_path)),

            # MFCCs
            **{f"mfcc{i+1}_mean": np.mean(mfcc[i]) for i in range(13)},
            **{f"mfcc{i+1}_std": np.std(mfcc[i]) for i in range(13)},

            # Global
            "centroid_mean": np.mean(centroid),
            "centroid_std": np.std(centroid),
            "rolloff_mean": np.mean(rolloff),
            "rolloff_std": np.std(rolloff),
            "bandwidth_mean": np.mean(bandwidth),
            "bandwidth_std": np.std(bandwidth),

            # Harmonic
            **{f"harmonic_chroma{i+1}_mean": np.mean(chroma[i]) for i in range(chroma.shape[0])},
            **{f"harmonic_chroma{i+1}_std": np.std(chroma[i]) for i in range(chroma.shape[0])},
            **{f"harmonic_tonnetz{i+1}_mean": np.mean(tonnetz[i]) for i in range(tonnetz.shape[0])},
            **{f"harmonic_tonnetz{i+1}_std": np.std(tonnetz[i]) for i in range(tonnetz.shape[0])},

            # Percussive
            "percussive_zcr_mean": np.mean(zcr),
            "percussive_zcr_std": np.std(zcr),
            "percussive_flatness_mean": np.mean(flatness),
            "percussive_flatness_std": np.std(flatness),
            "percussive_rms_mean": np.mean(rms),
            "percussive_rms_std": np.std(rms),

        }

        return features

    except Exception as e:
        print(f"Erro ao processar {file_path}: {e}")
        return None

def main():
    feature_rows = []
    for style_dir in os.listdir(RAW_DIR):
        full_dir = os.path.join(RAW_DIR, style_dir)
        if not os.path.isdir(full_dir):
            continue
        for filename in tqdm(os.listdir(full_dir), desc=f"Processando {style_dir}"):
            if filename.endswith(".wav"):
                path = os.path.join(full_dir, filename)
                feats = extract_features_from_hpss(path)
                if feats:
                    feature_rows.append(feats)

    df = pd.DataFrame(feature_rows)
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Features salvas em: {OUTPUT_CSV}")

main()
