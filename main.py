import os
import threading
import flet as ft



def main(page: ft.Page):
    page.title = "YouTube Downloader"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    if os.path.exists("/storage/emulated/0/Download"):
        carpeta = "/storage/emulated/0/Download"
    else:
        carpeta = os.path.join(os.path.expanduser("~"), "Downloads")

    url_box = ft.TextField(
        label="Enlace de YouTube",
        hint_text="https://youtu.be/...",
        width=350,
        border_radius=10,
    )

    estado = ft.Text("Listo para descargar", size=14)
    barra = ft.ProgressBar(width=350, visible=False)

    def hook(d):
        if d["status"] == "downloading":
            pct = d.get("_percent_str", "0%").strip()
            estado.value = f"Descargando... {pct}"
            page.update()
        elif d["status"] == "finished":
            estado.value = "Procesando archivo..."
            page.update()

    def descargar(link):
        import yt_dlp
        opts = opts = {
            "format": "best/bv*+ba/b",
            "outtmpl": os.path.join(carpeta, "%(title)s.%(ext)s"),
            "progress_hooks": [hook],
            "noplaylist": True,
            "extractor_args": {
                "youtube": {
                    "player_client": ["android", "web"],
                }
            },
        }

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(link, download=False)
                titulo = info.get("title", "Video de YouTube")
                estado.value = f"Iniciando: {titulo}"
                page.update()
                ydl.download([link])

            estado.value = f"¡Listo! Guardado en Descargas:\n{titulo}"
        except Exception as e:
            estado.value = f"Error: {e}"
        finally:
            barra.visible = False
            btn.disabled = False
            page.update()

    def al_pulsar(e):
        link = url_box.value.strip()
        if not link:
            estado.value = "Ingresa un enlace válido."
            page.update()
            return

        btn.disabled = True
        barra.visible = True
        estado.value = "Obteniendo información..."
        page.update()

        threading.Thread(target=descargar, args=(link,), daemon=True).start()

    btn = ft.Button("Descargar MP4", on_click=al_pulsar, width=200, height=45)

    page.add(
        ft.Text("YouTube Downloader", size=24, weight=ft.FontWeight.BOLD),
        url_box,
        btn,
        barra,
        estado,
    )


ft.run(main)