import pandas as pd
import os
import yt_dlp

# Caminho para a planilha com metadados das músicas
csv_path = "../data/music_dataset.csv"

# Diretório onde os áudios serão salvos
output_dir = "../data/raw"
os.makedirs(output_dir, exist_ok=True)

# Carregar a planilha
df = pd.read_csv(csv_path)

# Gerar lista de (link, caminho de saída)
downloads = []
for _, row in df.iterrows():
    artist_clean = row["artist"].lower().replace(" ", "_").replace("&", "and")
    title_clean = row["track_title"].lower().replace(" ", "_").replace("&", "and")
    country = row["country"].lower().replace(" ", "_")
    style = row["style"].lower().replace(" ", "_")
    filename = f"{country}_{style}_{artist_clean}_{title_clean}.%(ext)s"
    filepath = os.path.join(output_dir, filename)
    downloads.append((row["link"], filepath))

# Função para baixar e converter áudio
def download_audio(link, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
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
        print(f"Erro ao baixar {link}: {e}")

# Loop de download
for link, output_path in downloads:
    print(f"Baixando: {output_path}")
    download_audio(link, output_path)
