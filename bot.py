import json
import os
import re

import discord
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing from environment variables")


# =========================
# Configuration
# =========================

DEFAULT_PREFIX = "kk"
PREFIX_FILE = "prefixes.json"

COMMAND_PREFIX = "!"


# =========================
# Prefix storage
# =========================

def load_prefixes() -> dict:
    if not os.path.exists(PREFIX_FILE):
        return {}

    try:
        with open(PREFIX_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict):
            return data

    except (json.JSONDecodeError, OSError):
        pass

    return {}


def save_prefixes(prefixes: dict):
    with open(PREFIX_FILE, "w", encoding="utf-8") as file:
        json.dump(prefixes, file, indent=2)


prefixes = load_prefixes()


def get_prefix(guild_id: int) -> str:
    return prefixes.get(str(guild_id), DEFAULT_PREFIX)


# =========================
# Instagram URL handling
# =========================

INSTAGRAM_REGEX = re.compile(
    r"https?://(?:www\.)?instagram\.com/"
    r"(reel|p|tv)/"
    r"([^/?\s]+)"
    r"(?:/)?(?:\?[^\s]*)?",
    re.IGNORECASE,
)


def convert_instagram_urls(text: str, prefix: str) -> tuple[str, bool]:
    changed = False

    def replace(match: re.Match) -> str:
        nonlocal changed
        changed = True

        post_type = match.group(1)
        post_id = match.group(2)

        return f"https://www.{prefix}instagram.com/{post_type}/{post_id}/"

    new_text = INSTAGRAM_REGEX.sub(replace, text)

    return new_text, changed


# =========================
# Discord setup
# =========================

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(
    intents=intents,
    command_prefix=COMMAND_PREFIX,
)


# =========================
# Events
# =========================

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("Bot is ready.")


@client.event
async def on_message(message: discord.Message):

    # Ignore bots, including ourselves
    if message.author.bot:
        return

    # =========================
    # !prefix command
    # =========================

    if message.content.startswith(f"{COMMAND_PREFIX}prefix"):

        parts = message.content.split()

        # !prefix
        if len(parts) == 1:

            if message.guild is None:
                await message.channel.send(
                    "This command can only be used inside a server."
                )
                return

            current_prefix = get_prefix(message.guild.id)

            await message.channel.send(
                f"Current Instagram prefix: `{current_prefix}`\n"
                f"Example: `https://www.{current_prefix}instagram.com/reel/...`"
            )
            return

        # Only administrators can change the prefix
        if message.guild is None:
            return

        new_prefix = parts[1].lower()

        # !prefix reset
        if new_prefix == "reset":
            prefixes.pop(str(message.guild.id), None)
            save_prefixes(prefixes)

            await message.channel.send(
                f"✅ Instagram prefix reset to `{DEFAULT_PREFIX}`."
            )
            return

        # Only allow simple letters/numbers
        if not re.fullmatch(r"[a-z0-9]+", new_prefix):
            await message.channel.send(
                "❌ Prefix can only contain letters and numbers."
            )
            return

        prefixes[str(message.guild.id)] = new_prefix
        save_prefixes(prefixes)

        await message.channel.send(
            f"✅ Instagram prefix changed to `{new_prefix}`.\n"
            f"New links will use `https://www.{new_prefix}instagram.com/`."
        )

        return

    # =========================
    # Instagram conversion
    # =========================

    # Only process messages inside servers
    if message.guild is None:
        return

    prefix = get_prefix(message.guild.id)

    new_content, changed = convert_instagram_urls(
        message.content,
        prefix,
    )

    if not changed:
        return

    try:

        # Delete original message
        await message.delete()

        # Create temporary webhook
        webhook = await message.channel.create_webhook(
            name="KK Instagram"
        )

        # Repost using original sender's name and avatar
        await webhook.send(
            content=new_content,
            username=message.author.display_name,
            avatar_url=message.author.display_avatar.url,
            wait=False,
        )

        # Remove temporary webhook
        await webhook.delete()

    except discord.Forbidden:
        print(
            f"Missing permissions in #{message.channel} "
            f"to delete/repost messages."
        )

    except discord.HTTPException as e:
        print(f"Discord API error: {e}")


# =========================
# Start bot
# =========================

client.run(TOKEN)
