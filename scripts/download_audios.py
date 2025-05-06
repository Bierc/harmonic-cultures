import pandas as pd
import os
import yt_dlp

# Carregar o dataset expandido
csv_path = "../data/music_dataset.csv"
df = pd.read_csv(csv_path)

# Criar diretório de destino se não existir
output_dir = "..//data/raw"
os.makedirs(output_dir, exist_ok=True)

# Gerar lista de tuplas com (link, nome do arquivo)
downloads = []
for _, row in df.iterrows():
    artist_clean = row["artist"].lower().replace(" ", "_").replace("&", "and")
    title_clean = row["track_title"].lower().replace(" ", "_").replace("&", "and")
    country = row["country"].lower().replace(" ", "_")
    style = row["style"].lower().replace(" ", "_")
    filename = f"{country}_{style}_{artist_clean}_{title_clean}.%(ext)s"
    filepath = os.path.join(output_dir, filename)
    downloads.append((row["link"], filepath))

# Exibir lista organizada de arquivos para baixar
downloads_df = pd.DataFrame(downloads, columns=["link", "output_path"])


def download_audio(link, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'quiet': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

# Baixar os áudios
download_audio(<nao sei o que colocar aqui para executar o download de todos os audios>)