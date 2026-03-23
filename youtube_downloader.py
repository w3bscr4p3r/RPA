import os
import threading
from io import BytesIO

import customtkinter as ctk
import requests
import yt_dlp
from PIL import Image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class DownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("YouTube Downloader Pro by Daniel Alves")
        self.geometry("720x600")

        self.download_path = os.getcwd()
        self.current_info = None

        self.build_ui()

    def build_ui(self):
        self.url_entry = ctk.CTkEntry(
            self, width=500, placeholder_text="Cole a URL do vídeo ou da playlist"
        )
        self.url_entry.pack(pady=10)

        self.preview_button = ctk.CTkButton(
            self, text="Carregar prévia", command=self.load_preview
        )
        self.preview_button.pack()

        self.thumbnail_label = ctk.CTkLabel(self, text="")
        self.thumbnail_label.pack(pady=10)

        self.title_label = ctk.CTkLabel(self, text="")
        self.title_label.pack()

        self.resolution_menu = ctk.CTkComboBox(self, values=["auto","720p","1080p"])
        self.resolution_menu.set("auto")
        self.resolution_menu.pack(pady=10)

        self.mp3_switch = ctk.CTkSwitch(self, text="Converter para MP3")
        self.mp3_switch.pack()

        self.progress = ctk.CTkProgressBar(self, width=400)
        self.progress.set(0)
        self.progress.pack(pady=20)

        self.status = ctk.CTkLabel(self, text="")
        self.status.pack()

        self.download_button = ctk.CTkButton(
            self, text="Baixar", command=self.start_download
        )
        self.download_button.pack(pady=20)

    def _set_status(self, text):
        self.after(0, lambda: self.status.configure(text=text))

    def load_preview(self):
        url = self.url_entry.get().strip()
        if not url:
            self._set_status("Informe uma URL válida.")
            return

        self.preview_button.configure(state="disabled")
        self._set_status("Carregando prévia...")

        def worker():
            try:
                ydl_opts = {"quiet": True, "noplaylist": True}

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)

                self.current_info = info
                self.after(0, lambda: self.title_label.configure(text=info.get("title", "")))

                thumb_url = info.get("thumbnail")
                if thumb_url:
                    response = requests.get(thumb_url, timeout=15)
                    response.raise_for_status()
                    img_data = response.content
                    img = Image.open(BytesIO(img_data)).resize((320, 180))
                    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(320, 180))
                    self.after(0, lambda: self.thumbnail_label.configure(image=ctk_img, text=""))
                    self.thumbnail_label.image = ctk_img

                formats = info.get("formats", [])
                heights = sorted(
                    {
                        int(f["height"])
                        for f in formats
                        if f.get("vcodec") != "none" and f.get("height")
                    }
                )
                resolutions = ["auto"] + [f"{h}p" for h in heights]

                self.after(0, lambda: self.resolution_menu.configure(values=resolutions))
                self.after(0, lambda: self.resolution_menu.set("auto"))
                self._set_status("Preview carregado.")
            except Exception as e:  # noqa: BLE001
                self._set_status(f"Erro ao carregar preview: {e}")
            finally:
                self.after(0, lambda: self.preview_button.configure(state="normal"))

        threading.Thread(target=worker, daemon=True).start()

    def progress_hook(self, data):
        status = data.get("status")
        if status == "downloading":
            percent_str = data.get("_percent_str")
            if percent_str:
                try:
                    percent = float(percent_str.replace("%", "").strip())
                    self.after(0, lambda: self.progress.set(percent / 100))
                except ValueError:
                    pass
        elif status == "finished":
            self._set_status("Processando...")

    def start_download(self):
        threading.Thread(target=self.download, daemon=True).start()

    def download(self):
        url = self.url_entry.get().strip()
        resolution = self.resolution_menu.get().strip() or "auto"

        if not url:
            self._set_status("Informe uma URL válida.")
            return

        self.after(0, lambda: self.progress.set(0))
        self._set_status("Baixando...")
        self.after(0, lambda: self.download_button.configure(state="disabled"))

        outtmpl = os.path.join(self.download_path, "%(title)s.%(ext)s")

        if self.mp3_switch.get():
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": outtmpl,
                "progress_hooks": [self.progress_hook],
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }
        else:
            if resolution == "auto":
                format_selector = "bestvideo+bestaudio/best"
            else:
                height = resolution.replace("p", "")
                format_selector = f"bestvideo[height<={height}]+bestaudio/best"

            ydl_opts = {
                "format": format_selector,
                "merge_output_format": "mkv",
                "outtmpl": outtmpl,
                "progress_hooks": [self.progress_hook],
            }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self._set_status("Download concluído")
            self.after(0, lambda: self.progress.set(1))
        except Exception as e:  # noqa: BLE001
            self._set_status(f"Erro no download: {e}")
        finally:
            self.after(0, lambda: self.download_button.configure(state="normal"))


if __name__ == "__main__":
    app = DownloaderApp()
    app.mainloop()
