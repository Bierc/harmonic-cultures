import sys
import yt_dlp
import os

def download_audio(link, output_name, output_dir="data/raw"):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{output_name}.%(ext)s")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'quiet': False,
        'ffmpeg_location': '/usr/bin/ffmpeg',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '0',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python download_music.py <youtube_url> <output_name>")
        sys.exit(1)

    url = sys.argv[1]
    output_name = sys.argv[2]
    download_audio(url, output_name)
