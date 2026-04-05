# RPA (Automação de Processos Robóticos)

Scripts de automação e produtividade em Python.

## Ferramentas

| Ferramenta | Descrição |
|------------|-----------|
| `organizador_de_arquivos.py` | Organiza arquivos automaticamente por extensão em pastas categorizadas. |
| `youtube_downloader.py` | Interface GUI para baixar vídeos e playlists do YouTube com opções de resolução e conversão para MP3. |
| `web_scraping.py` | Scraper da Wikipedia em português brasileiro com limite configurável de parágrafos. |

## Instalação

```bash
# Dependências gerais
pip install customtkinter pillow yt_dlp requests beautifulsoup4
```

## Uso

### Organizador de Arquivos

Organiza todos os arquivos do diretório atual em pastas por categoria:

```bash
python organizador_de_arquivos.py
```

**Categorias criadas automaticamente:**
- `PDF/` - Arquivos .pdf
- `Word/` - Arquivos .doc, .docx, .txt
- `Excel/` - Arquivos .xls, .xlsx, .csv
- `PowerPoint/` - Arquivos .ppt, .pptx
- `Imagens/` - Arquivos .jpg, .jpeg, .png
- `Programas/` - Arquivos .exe, .msi
- `Compactados/` - Arquivos .zip, .rar, .iso

### YouTube Downloader

Interface gráfica para download de vídeos:

```bash
python youtube_downloader.py
```

**Recursos:**
- Cole a URL do vídeo ou playlist
- Preview com thumbnail e título
- Seleção de resolução (auto, 720p, 1080p)
- Conversão opcional para MP3
- Barra de progresso em tempo real

### Web Scraping (Wikipedia)

```bash
python web_scraping.py
```

**Configuração:** Edite o script para definir:
- URL do artigo da Wikipedia
- Número máximo de parágrafos para extrair
- Nome do arquivo de saída

## Dependências

```txt
customtkinter>=5.0
pillow>=9.0
yt_dlp>=2023.0
requests>=2.28
beautifulsoup4>=4.11
```
