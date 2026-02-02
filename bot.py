import os
import hashlib
import secrets
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from datetime import datetime
import pytz
from environment import API_ID, API_HASH, BOT_TOKEN, DEFAULT_THUMBNAIL, SECRET_KEY, MONGO_URI, ADMIN_IDS, PORT

from pymongo import MongoClient

# Optional: MongoDB setup
if MONGO_URI:
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client.get_database("secure_html_bot")
    users_col = db["users"]
else:
    db = None
    users_col = None

# Admin list
ADMIN_IDS = [int(i.strip()) for i in ADMIN_IDS.split(",")] if ADMIN_IDS else []

# Initialize Telegram client
app = Client(
    "secure_html_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    parse_mode=enums.ParseMode.HTML
)

# ---------------- UTILITY FUNCTIONS ----------------

def generate_access_code():
    """Generate a secure access code for users"""
    return f"ER.BABU{{{''.join(secrets.choice('0123456789') for _ in range(6))}}}"

def categorize_urls(urls):
    """Simple categorization: videos / pdfs / others"""
    videos, pdfs, others = [], [], []
    for name, url in urls:
        url_lower = url.lower()
        if "classplusapp" in url_lower:
            videos.append((name, f"https://engineers-babu.onrender.com/?url={url}"))
        elif ".zip" in url_lower:
            videos.append((name, url))
        elif any(x in url_lower for x in ["youtube.com", "youtu.be"]):
            videos.append((name, url))
        elif any(ext in url_lower for ext in [".mp4", ".mkv", ".webm", ".avi", ".mov"]):
            videos.append((name, url))
        elif ".pdf" in url_lower:
            pdfs.append((name, url))
        else:
            others.append((name, url))
    return videos, pdfs, others

def extract_names_and_urls(file_content):
    """Extract name:url pairs from .txt content"""
    urls = []
    for line in file_content.strip().split("\n"):
        if ":" in line:
            name, url = line.split(":", 1)
            urls.append((name.strip(), url.strip()))
    return urls

def generate_html(file_name, urls):
    """Generate HTML with glassmorphism + mobile-first design"""
    base_name = os.path.splitext(file_name)[0]
    videos, pdfs, others = categorize_urls(urls)
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist).strftime("%d %B %Y | %I:%M:%S %p")

    video_html = "".join(f"<li>{name}: <a href='{url}' target='_blank'>{url}</a></li>" for name, url in videos)
    pdf_html = "".join(f"<li>{name}: <a href='{url}' target='_blank'>{url}</a></li>" for name, url in pdfs)
    other_html = "".join(f"<li>{name}: <a href='{url}' target='_blank'>{url}</a></li>" for name, url in others)

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{base_name}</title>
<style>
body {{
    background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05)), url('https://i.postimg.cc/4N69wBLt/hat-hacker.webp') no-repeat center center fixed;
    backdrop-filter: blur(10px);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #fff;
    padding: 20px;
}}
.container {{
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 20px;
    max-width: 800px;
    margin: auto;
}}
h1 {{ text-align: center; margin-bottom: 20px; }}
h2 {{ margin-top: 20px; color: #fffb; }}
ul {{ list-style-type: none; padding: 0; }}
li {{ padding: 8px 0; }}
a {{ color: #ffd700; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
@media(max-width:768px) {{
    .container {{ padding: 15px; }}
}}
</style>
</head>
<body>
<div class="container">
<h1>{base_name}</h1>
<p>Generated: {now}</p>
<h2>Videos</h2><ul>{video_html}</ul>
<h2>PDFs</h2><ul>{pdf_html}</ul>
<h2>Others</h2><ul>{other_html}</ul>
</div>
</body>
</html>
"""

# ---------------- BOT HANDLERS ----------------

@app.on_message(filters.private & filters.document & filters.incoming)
async def txt_to_html(client: Client, message: Message):
    """Convert uploaded .txt file to HTML"""
    file_name = message.document.file_name
    if not file_name.endswith(".txt"):
        await message.reply_text("❌ Only .txt files are supported.")
        return

    file_path = await message.download()
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    urls = extract_names_and_urls(content)
    html_content = generate_html(file_name, urls)

    html_file_name = file_name.replace(".txt", ".html")
    with open(html_file_name, "w", encoding="utf-8") as f:
        f.write(html_content)

    await message.reply_document(
        document=html_file_name,
        caption=f"✅ Converted {file_name} → {html_file_name}"
    )

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text(
        "👋 Welcome! Send me a .txt file in the format `Name:URL` per line and I will convert it to a beautiful HTML page."
    )

# ---------------- RUN BOT ----------------
if __name__ == "__main__":
    print(f"Bot is starting on port {PORT}...")
    app.run()
