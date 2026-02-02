import os

def get_env(name: str, required=True, cast=None):
    value = os.getenv(name)
    if value is None:
        if required:
            raise RuntimeError(f"❌ Missing environment variable: {name}")
        return None
    if cast:
        try:
            return cast(value)
        except Exception:
            raise RuntimeError(f"❌ Invalid value for {name}")
    return value

# Telegram credentials
API_ID = get_env("API_ID", cast=int)
API_HASH = get_env("API_HASH")
BOT_TOKEN = get_env("BOT_TOKEN")

# MongoDB
MONGO_URI = get_env("MONGO_URI", required=False)

# Default Thumbnail & other settings
DEFAULT_THUMBNAIL = get_env("DEFAULT_THUMBNAIL", required=False)
SECRET_KEY = get_env("SECRET_KEY", required=False)
CHANNEL_ID = get_env("CHANNEL_ID", required=False)
ADMIN_IDS = get_env("ADMIN_IDS", required=False)  # comma-separated
PORT = get_env("PORT", cast=int, required=False) or 10000
