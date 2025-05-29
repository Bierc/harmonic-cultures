import pandas as pd
import os
import yt_dlp

# Caminho para a planilha com metadados das músicas
csv_path = r"C:\Users\psene\git\harmonic-cultures\data\music_dataset_120_full.csv"

# Diretório onde os áudios serão salvos
output_dir = r"C:\Users\psene\git\harmonic-cultures\data\raw"
os.makedirs(output_dir, exist_ok=True)

# Carregar a planilha
df = pd.read_csv(csv_path)

# Loop para preparar e baixar músicas
for _, row in df.iterrows():
    link = row.get("link", "")
    if pd.isna(link) or not isinstance(link, str) or link.strip() == "":
        print("⏭️  Música sem link. Pulando.")
        continue

    # Nome de arquivo formatado
    artist_clean = row["artist"].lower().replace(" ", "_").replace("&", "and")
    title_clean = row["track_title"].lower().replace(" ", "_").replace("&", "and")
    country = row["country"].lower().replace(" ", "_")
    style = row["style"].lower().replace(" ", "_")
    filename = f"{country}_{style}_{artist_clean}_{title_clean}.wav"
    full_path = os.path.join(output_dir, filename)

    # Verificar se já foi baixado
 #   if os.path.exists(full_path):
  #      print(f"✅ Já existe: {filename}. Pulando download.")
   #     continue

    # Baixar e converter para WAV
    print(f"⬇️  Baixando: {filename}")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, f"{country}_{style}_{artist_clean}_{title_clean}.%(ext)s"),
        'quiet': False,
        'ffmpeg_location': 'C:/Users/psene/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-7.1.1-full_build/bin',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '0',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
    except Exception as e:
        print(f"❌ Erro ao baixar {link}: {e}")
