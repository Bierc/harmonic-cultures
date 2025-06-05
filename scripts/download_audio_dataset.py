import pandas as pd
import os
import yt_dlp
import shutil

# Caminhos
csv_path = "/home/satan/git/harmonic-cultures/data/raw_subsets/subset_metadata.csv"
raw_dir = "/home/satan/git/harmonic-cultures/data/raw_subsets/raw"
os.makedirs(raw_dir, exist_ok=True)

# Subpastas por estilo
base_dir = os.path.dirname(raw_dir)
styles = ["samba", "jazz", "afrobeat"]
style_dirs = {style: os.path.join(base_dir, style) for style in styles}
for dir_path in style_dirs.values():
    os.makedirs(dir_path, exist_ok=True)

# Carregar CSV
df = pd.read_csv(csv_path)

# Loop de download e organização
for _, row in df.iterrows():
    link = row.get("link", "")
    style = row.get("style", "").strip().lower()

    if style not in style_dirs:
        print(f"❌ Estilo desconhecido: {style}. Pulando.")
        continue

    if pd.isna(link) or not isinstance(link, str) or link.strip() == "":
        print("⏭️  Música sem link. Pulando.")
        continue

    # Nome do arquivo formatado
    artist_clean = row["artist"].lower().replace(" ", "_").replace("&", "and")
    title_clean = row["track_title"].lower().replace(" ", "_").replace("&", "and")
    country = row["country"].lower().replace(" ", "_")
    filename = f"{country}_{style}_{artist_clean}_{title_clean}.wav"

    output_path = os.path.join(raw_dir, filename)
    final_path = os.path.join(style_dirs[style], filename)

    # Se já existe no destino final, pula
    if os.path.exists(final_path):
        print(f"✅ Já existe: {filename}. Pulando download.")
        continue

    print(f"⬇️  Baixando: {filename}")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(raw_dir, f"{country}_{style}_{artist_clean}_{title_clean}.%(ext)s"),
        'quiet': False,
        'ffmpeg_location': '/usr/bin/ffmpeg',
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
        print(f"❌ Erro ao baixar {filename}: {e}")
        continue

    # Move o arquivo final
    if os.path.exists(output_path):
        shutil.move(output_path, final_path)
        print(f"📁 Movido para: {final_path}")
    else:
        print(f"⚠️ Arquivo não encontrado após download: {output_path}")
