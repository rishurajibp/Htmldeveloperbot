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


# ✅ Telegram credentials (ENV NAMES, NOT VALUES)
API_ID = 21705536
API_HASH = "c5bb241f6e3ecf33fe68a444e288de2d"
BOT_TOKEN = get_env("BOT_TOKEN")
