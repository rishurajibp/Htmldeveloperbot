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


# ✅ Correct usage — use ENV variable names, not values
API_ID = get_env("API_ID", cast=int)
API_HASH = get_env("API_HASH")
BOT_TOKEN = get_env("BOT_TOKEN")
