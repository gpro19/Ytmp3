#!/data/data/com.termux/files/usr/bin/python
import yt_dlp
import os
import sys
from pathlib import Path

# Warna untuk tampilan
class Color:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def clear_screen():
    os.system('clear')

def print_banner():
    banner = f"""
{Color.CYAN}╔══════════════════════════════════════════╗
║     YOUTUBE PLAYLIST MP3 DOWNLOADER      ║
║           Simple & Easy to Use           ║
╚══════════════════════════════════════════╝{Color.END}
"""
    print(banner)

def print_success(msg):
    print(f"{Color.GREEN}✅ {msg}{Color.END}")

def print_error(msg):
    print(f"{Color.RED}❌ {msg}{Color.END}")

def print_info(msg):
    print(f"{Color.BLUE}ℹ️  {msg}{Color.END}")

def progress_hook(d):
    if d['status'] == 'downloading':
        try:
            percentage = d.get('_percent_str', '0%')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            
            # Progress bar
            percent = float(percentage.replace('%', ''))
            bar_length = 30
            filled = int(bar_length * percent // 100)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            print(f"\r{Color.CYAN}⬇️  [{bar}] {percentage} | ⚡{speed} | ⏳{eta}{Color.END}", end='', flush=True)
        except:
            pass
    elif d['status'] == 'finished':
        print(f"\n{Color.GREEN}✅ Download selesai, konversi ke MP3...{Color.END}")

def download_playlist(url, quality='192', output_dir='music'):
    """Download playlist dengan pengaturan sederhana"""
    
    # Tentukan lokasi penyimpanan
    if output_dir == 'music':
        base_path = os.path.join(str(Path.home()), 'storage', 'music', 'YouTube')
    elif output_dir == 'downloads':
        base_path = os.path.join(str(Path.home()), 'storage', 'downloads', 'YouTube')
    else:
        base_path = output_dir
    
    os.makedirs(base_path, exist_ok=True)
    
    print_info(f"Lokasi penyimpanan: {base_path}")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': quality,
        }],
        'outtmpl': os.path.join(base_path, '%(playlist_title)s', '%(title)s.%(ext)s'),
        'ignoreerrors': True,
        'no_warnings': True,
        'quiet': False,
        'progress_hooks': [progress_hook],
        'noplaylist': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Ambil info playlist
            print_info("Mengambil info playlist...")
            info = ydl.extract_info(url, download=False)
            
            if 'entries' in info:
                total = len(info['entries'])
                print_success(f"Playlist: {info.get('title', 'Unknown')}")
                print_success(f"Total video: {total}")
                
                # Tampilkan daftar video
                print(f"\n{Color.YELLOW}Daftar Video:{Color.END}")
                for i, entry in enumerate(info['entries'], 1):
                    duration = entry.get('duration', 0)
                    minutes = int(duration // 60) if duration else 0
                    seconds = int(duration % 60) if duration else 0
                    print(f"  {i}. {entry.get('title', 'Unknown')[:50]} ({minutes}:{seconds:02d})")
                
                print(f"\n{Color.BOLD}Mulai download? (y/n){Color.END}")
                if input().lower() != 'y':
                    print_info("Download dibatalkan")
                    return
            
            # Download
            print_info("Memulai download...")
            ydl.download([url])
            print_success(f"Download selesai! File tersimpan di: {base_path}")
            
    except Exception as e:
        print_error(f"Error: {str(e)}")

def main():
    while True:
        clear_screen()
        print_banner()
        
        print(f"{Color.YELLOW}📋 MENU UTAMA:{Color.END}")
        print("1. 🎵 Download Playlist ke Music")
        print("2. 📥 Download Playlist ke Downloads")
        print("3. 📝 Lihat Daftar Video")
        print("4. ⚙️  Pengaturan")
        print("5. ❌ Keluar")
        
        choice = input(f"\n{Color.BOLD}Pilih menu (1-5): {Color.END}").strip()
        
        if choice == '1':
            clear_screen()
            print_banner()
            url = input("🔗 Masukkan URL playlist YouTube: ").strip()
            if url:
                quality = input("🎵 Kualitas audio (128/192/320, default 192): ").strip() or '192'
                download_playlist(url, quality, 'music')
                input(f"\n{Color.BOLD}Tekan Enter untuk kembali...{Color.END}")
        
        elif choice == '2':
            clear_screen()
            print_banner()
            url = input("🔗 Masukkan URL playlist YouTube: ").strip()
            if url:
                quality = input("🎵 Kualitas audio (128/192/320, default 192): ").strip() or '192'
                download_playlist(url, quality, 'downloads')
                input(f"\n{Color.BOLD}Tekan Enter untuk kembali...{Color.END}")
        
        elif choice == '3':
            clear_screen()
            print_banner()
            url = input("🔗 Masukkan URL playlist YouTube: ").strip()
            if url:
                # Tampilkan daftar video
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'extract_flat': True,
                }
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=False)
                        if 'entries' in info:
                            print(f"\n{Color.YELLOW}Playlist: {info.get('title', 'Unknown')}{Color.END}")
                            print(f"{Color.YELLOW}Total: {len(info['entries'])} video{Color.END}")
                            print("-" * 50)
                            for i, entry in enumerate(info['entries'], 1):
                                print(f"{i:3d}. {entry.get('title', 'Unknown')[:60]}")
                except Exception as e:
                    print_error(f"Error: {str(e)}")
                input(f"\n{Color.BOLD}Tekan Enter untuk kembali...{Color.END}")
        
        elif choice == '4':
            clear_screen()
            print_banner()
            print(f"{Color.YELLOW}⚙️  PENGATURAN:{Color.END}")
            print("1. Set kualitas default")
            print("2. Set lokasi default")
            print("3. Update yt-dlp")
            print("4. Kembali")
            
            setting = input(f"\n{Color.BOLD}Pilih pengaturan: {Color.END}").strip()
            
            if setting == '3':
                print_info("Updating yt-dlp...")
                os.system('pip install --upgrade yt-dlp')
                print_success("yt-dlp berhasil diupdate!")
                input(f"\n{Color.BOLD}Tekan Enter untuk kembali...{Color.END}")
        
        elif choice == '5':
            clear_screen()
            print_success("Terima kasih! Sampai jumpa! 👋")
            sys.exit()
        
        else:
            print_error("Pilihan tidak valid!")
            input(f"\n{Color.BOLD}Tekan Enter untuk melanjutkan...{Color.END}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print_success("Program dihentikan. Sampai jumpa! 👋")
        sys.exit()
