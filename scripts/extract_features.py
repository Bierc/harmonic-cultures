import os
import librosa
import numpy as np
import pandas as pd

RAW_DIR = "data/raw"
OUTPUT_CSV = "data/features_audio.csv"
DURATION = 60  # segundos

def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path, sr=22050)
        if len(y) > DURATION * sr:
            y = y[:DURATION * sr]  # força corte de 60 segundos

        features = {
            "filename": os.path.basename(file_path),
            "mfcc_mean": np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13), axis=1).tolist(),
            "mfcc_std": np.std(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13), axis=1).tolist(),
            "centroid_mean": np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)),
            "centroid_std": np.std(librosa.feature.spectral_centroid(y=y, sr=sr)),
            "rolloff_mean": np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)),
            "rolloff_std": np.std(librosa.feature.spectral_rolloff(y=y, sr=sr)),
            "zcr_mean": np.mean(librosa.feature.zero_crossing_rate(y)),
            "zcr_std": np.std(librosa.feature.zero_crossing_rate(y)),
            "flatness_mean": np.mean(librosa.feature.spectral_flatness(y=y)),
            "flatness_std": np.std(librosa.feature.spectral_flatness(y=y))
        }
        return features
    except Exception as e:
        print(f"Erro ao processar {file_path}: {e}")
        return None

def main():
    feature_rows = []
    for filename in os.listdir(RAW_DIR):
        if filename.endswith(".wav"):
            path = os.path.join(RAW_DIR, filename)
            print(f"Processando: {filename}")
            feats = extract_features(path)
            if feats:
                feature_rows.append(feats)

    # Expand MFCCs para colunas separadas
    df = pd.DataFrame(feature_rows)
    if "mfcc_mean" in df.columns:
        mfcc_means = pd.DataFrame(df["mfcc_mean"].tolist(), columns=[f"mfcc{i+1}_mean" for i in range(13)])
        mfcc_stds = pd.DataFrame(df["mfcc_std"].tolist(), columns=[f"mfcc{i+1}_std" for i in range(13)])
        df = pd.concat([df.drop(["mfcc_mean", "mfcc_std"], axis=1), mfcc_means, mfcc_stds], axis=1)

    os.makedirs("data", exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Features salvas em: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
