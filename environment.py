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
API_ID = get_env("21705536", cast=int)
API_HASH = get_env("c5bb241f6e3ecf33fe68a444e288de2d")
BOT_TOKEN = get_env("7601635113:AAG_bPYt03h1AdHcz-bMnPdnvFW9GHgC5g8")
