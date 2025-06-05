import os
import librosa
import numpy as np
import pandas as pd

BASE_DIR = "data/raw_subsets"
OUTPUT_CSV = "data/features_audio.csv"
DURATION = 60  # segundos

def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path, sr=22050)
        if len(y) > DURATION * sr:
            y = y[:DURATION * sr]  # corta se exceder DURATION

        features = {
            "filename": os.path.basename(file_path),
            "style": os.path.basename(os.path.dirname(file_path)),
            "track_id": os.path.splitext(os.path.basename(file_path))[0],

            "mfcc_mean": np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13), axis=1).tolist(),
            "mfcc_std": np.std(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13), axis=1).tolist(),

            "centroid_mean": np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)),
            "centroid_std": np.std(librosa.feature.spectral_centroid(y=y, sr=sr)),

            "rolloff_mean": np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)),
            "rolloff_std": np.std(librosa.feature.spectral_rolloff(y=y, sr=sr)),

            "zcr_mean": np.mean(librosa.feature.zero_crossing_rate(y)),
            "zcr_std": np.std(librosa.feature.zero_crossing_rate(y)),

            "flatness_mean": np.mean(librosa.feature.spectral_flatness(y=y)),
            "flatness_std": np.std(librosa.feature.spectral_flatness(y=y)),

            "chroma_stft_mean": np.mean(librosa.feature.chroma_stft(y=y, sr=sr), axis=1).tolist(),
            "chroma_stft_std": np.std(librosa.feature.chroma_stft(y=y, sr=sr), axis=1).tolist(),

            "tonnetz_mean": np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr), axis=1).tolist(),
            "tonnetz_std": np.std(librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr), axis=1).tolist(),

            "bandwidth_mean": np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)),
            "bandwidth_std": np.std(librosa.feature.spectral_bandwidth(y=y, sr=sr)),

            "rms_mean": np.mean(librosa.feature.rms(y=y)),
            "rms_std": np.std(librosa.feature.rms(y=y)),
        }

        return features
    except Exception as e:
        print(f"⚠️ Erro ao processar {file_path}: {e}")
        return None

def main():
    feature_rows = []
    for style_folder in os.listdir(BASE_DIR):
        subdir = os.path.join(BASE_DIR, style_folder)
        if not os.path.isdir(subdir):
            continue
        for filename in os.listdir(subdir):
            if filename.endswith(".wav"):
                path = os.path.join(subdir, filename)
                print(f"🎧 Processando: {path}")
                feats = extract_features(path)
                if feats:
                    feature_rows.append(feats)

    df = pd.DataFrame(feature_rows)

    # Expandir colunas de lista (MFCC, chroma, etc.)
    if "mfcc_mean" in df.columns:
        mfcc_means = pd.DataFrame(df["mfcc_mean"].tolist(), columns=[f"mfcc{i+1}_mean" for i in range(13)])
        mfcc_stds = pd.DataFrame(df["mfcc_std"].tolist(), columns=[f"mfcc{i+1}_std" for i in range(13)])
        df = pd.concat([df.drop(["mfcc_mean", "mfcc_std"], axis=1), mfcc_means, mfcc_stds], axis=1)

    if "chroma_stft_mean" in df.columns:
        chroma_means = pd.DataFrame(df["chroma_stft_mean"].tolist(), columns=[f"chroma{i+1}_mean" for i in range(12)])
        chroma_stds = pd.DataFrame(df["chroma_stft_std"].tolist(), columns=[f"chroma{i+1}_std" for i in range(12)])
        df = pd.concat([df.drop(["chroma_stft_mean", "chroma_stft_std"], axis=1), chroma_means, chroma_stds], axis=1)

    if "tonnetz_mean" in df.columns:
        tonnetz_means = pd.DataFrame(df["tonnetz_mean"].tolist(), columns=[f"tonnetz{i+1}_mean" for i in range(6)])
        tonnetz_stds = pd.DataFrame(df["tonnetz_std"].tolist(), columns=[f"tonnetz{i+1}_std" for i in range(6)])
        df = pd.concat([df.drop(["tonnetz_mean", "tonnetz_std"], axis=1), tonnetz_means, tonnetz_stds], axis=1)

    os.makedirs("data", exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Features salvas em: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
