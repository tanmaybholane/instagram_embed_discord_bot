import os
import re

import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing from .env")


# Matches:
# https://instagram.com/reel/ABC123/
# https://www.instagram.com/reel/ABC123/?stkn=XYZ
# https://instagram.com/p/ABC123
# https://www.instagram.com/tv/ABC123/
INSTAGRAM_REGEX = re.compile(
    r"https?://(?:www\.)?instagram\.com/"
    r"(reel|p|tv)/"
    r"([^/?\s]+)"
    r"(?:/)?(?:\?[^\s]*)?",
    re.IGNORECASE,
)


def convert_instagram_urls(text: str) -> tuple[str, bool]:
    """
    Replace Instagram URLs with kkinstagram URLs.

    Example:
    https://www.instagram.com/reel/ABC/?stkn=XYZ
    ->
    https://www.kkinstagram.com/reel/ABC/
    """

    changed = False

    def replace(match: re.Match) -> str:
        nonlocal changed
        changed = True

        post_type = match.group(1)
        post_id = match.group(2)

        return f"https://www.kkinstagram.com/{post_type}/{post_id}/"

    new_text = INSTAGRAM_REGEX.sub(replace, text)

    return new_text, changed


# Discord configuration
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("Bot is ready.")


@client.event
async def on_message(message: discord.Message):

    # Ignore messages sent by bots
    if message.author.bot:
        return

    # Convert Instagram URLs
    new_content, changed = convert_instagram_urls(message.content)

    # Nothing to do
    if not changed:
        return

    try:
        # Delete the original message
        await message.delete()

        # Repost it while preserving the sender's identity
        #
        # The bot cannot literally send a message as the user,
        # so we display their name and avatar using a webhook-style embed.
        webhook = await message.channel.create_webhook(
            name="KK Instagram"
        )

        await webhook.send(
            content=new_content,
            username=message.author.display_name,
            avatar_url=message.author.display_avatar.url,
            wait=False,
        )

        # Delete the temporary webhook.
        await webhook.delete()

    except discord.Forbidden:
        print(
            f"Missing permissions in #{message.channel} "
            f"to delete/repost messages."
        )

    except discord.HTTPException as e:
        print(f"Discord API error: {e}")


client.run(TOKEN)

