import os
from datetime import datetime
from urllib.parse import quote_plus

from pyrogram import Client, filters
from pyrogram.types import Message

# =========================
# ENV VARIABLES (Koyeb)
# =========================
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# =========================
# BOT INIT
# =========================
bot = Client(
    "txt_to_html_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# =========================
# URL CATEGORIZATION
# =========================
def categorize_urls(urls):
    videos, pdfs, others = [], [], []

    VIDEO_EXTENSIONS = (
        ".m3u8", ".mp4", ".mkv", ".webm",
        ".avi", ".mov", ".wmv", ".flv",
        ".mpeg", ".mpd"
    )

    YOUTUBE_KEYS = (
        "youtube.com/watch",
        "youtube.com/embed",
        "youtu.be"
    )

    for name, url in urls:
        url_lower = url.lower()

        # ClassPlus
        if "classplusapp" in url_lower:
            encoded = quote_plus(url)
            videos.append((
                name,
                f"https://engineersbabuplayer.onrender.com/?url={encoded}"
            ))

        # ZIP (AppX batch)
        elif url_lower.endswith(".zip"):
            encoded = quote_plus(url)
            videos.append((
                name,
                f"https://video.pablocoder.eu.org/appx-zip?url={encoded}"
            ))

        # YouTube
        elif any(k in url_lower for k in YOUTUBE_KEYS):
            videos.append((name, url))

        # Direct video
        elif url_lower.endswith(VIDEO_EXTENSIONS):
            videos.append((name, url))

        # PDF
        elif url_lower.endswith(".pdf"):
            pdfs.append((name, url))

        # Others
        else:
            others.append((name, url))

    return videos, pdfs, others


# =========================
# GLASSMORPHISM HTML
# =========================
def generate_html(videos, pdfs, others, title):
    def section(title, items, emoji):
        if not items:
            return ""
        cards = ""
        for name, url in items:
            cards += f"""
            <a href="{url}" class="card">
                <span class="emoji">{emoji}</span>
                <span>{name}</span>
            </a>
            """
        return f"""
        <section>
            <h2>{emoji} {title}</h2>
            <div class="grid">{cards}</div>
        </section>
        """

    time_now = datetime.now().strftime("%d %b %Y • %I:%M %p")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>

<style>
body {{
    margin: 0;
    font-family: system-ui, -apple-system, sans-serif;
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}}

.container {{
    max-width: 900px;
    margin: auto;
    padding: 16px;
}}

header {{
    backdrop-filter: blur(14px);
    background: rgba(255,255,255,0.12);
    border-radius: 18px;
    padding: 20px;
    text-align: center;
    margin-bottom: 22px;
}}

h1 {{
    margin: 0;
    font-size: 1.6rem;
}}

small {{
    opacity: 0.7;
}}

section {{
    margin-bottom: 26px;
}}

h2 {{
    font-size: 1.2rem;
    margin-bottom: 12px;
}}

.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 12px;
}}

.card {{
    display: flex;
    gap: 10px;
    align-items: center;
    padding: 14px;
    border-radius: 16px;
    text-decoration: none;
    color: white;
    backdrop-filter: blur(12px);
    background: rgba(255,255,255,0.15);
    transition: 0.25s;
}}

.card:hover {{
    background: rgba(255,255,255,0.28);
    transform: translateY(-3px);
}}

.emoji {{
    font-size: 1.4rem;
}}
</style>
</head>

<body>
<div class="container">

<header>
    <h1>{title}</h1>
    <small>{time_now}</small>
</header>

{section("Videos", videos, "🎬")}
{section("PDF Notes", pdfs, "📘")}
{section("Others", others, "📁")}

</div>
</body>
</html>
"""


# =========================
# TXT → HTML HANDLER
# =========================
@bot.on_message(filters.private & filters.document)
async def txt_converter(_, message: Message):
    if not message.document.file_name.endswith(".txt"):
        return await message.reply("❌ Please send a `.txt` file only.")

    path = await message.download()

    urls = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if "|" in line:
                name, url = line.split("|", 1)
                urls.append((name.strip(), url.strip()))

    videos, pdfs, others = categorize_urls(urls)

    html = generate_html(
        videos, pdfs, others,
        title="Engineers Babu Library"
    )

    html_path = path.replace(".txt", ".html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    await message.reply_document(
        html_path,
        caption="✨ TXT → HTML converted (Glass UI)"
    )


# =========================
# START BOT
# =========================
bot.run()
