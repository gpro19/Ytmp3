#!/data/data/com.termux/files/usr/bin/bash

# YouTube Playlist Downloader - Simple Version

clear

echo "=========================================="
echo "   YOUTUBE PLAYLIST MP3 DOWNLOADER"
echo "=========================================="
echo ""

# Input URL
read -p "🔗 Tempel URL playlist: " url

if [ -z "$url" ]; then
    echo "❌ URL tidak boleh kosong!"
    exit 1
fi

echo ""
echo "Pilih kualitas:"
echo "1. Hemat (128kbps)"
echo "2. Standar (192kbps)"
echo "3. Tinggi (320kbps)"
read -p "Pilih (1-3, default 2): " quality

case $quality in
    1) kbps="128" ;;
    3) kbps="320" ;;
    *) kbps="192" ;;
esac

echo ""
echo "Pilih lokasi:"
echo "1. Music"
echo "2. Downloads"
read -p "Pilih (1-2, default 1): " location

if [ "$location" = "2" ]; then
    folder="$HOME/storage/downloads/YouTube"
else
    folder="$HOME/storage/music/YouTube"
fi

mkdir -p "$folder"

echo ""
echo "📥 Memulai download..."
echo "📁 Lokasi: $folder"
echo "🎵 Kualitas: $kbps kbps"
echo ""

# Download playlist
yt-dlp \
    -x \
    --audio-format mp3 \
    --audio-quality "$kbps" \
    -o "$folder/%(playlist_title)s/%(title)s.%(ext)s" \
    --ignore-errors \
    --no-warnings \
    --newline \
    "$url"

echo ""
echo "=========================================="
echo "✅ Download selesai!"
echo "📁 Cek folder: $folder"
echo "=========================================="
