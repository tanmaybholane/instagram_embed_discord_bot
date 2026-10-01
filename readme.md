# KK Instagram

A lightweight Discord bot that automatically transforms Instagram links into embeddable `kkinstagram.com` links, allowing users to preview and watch Instagram Reels and other supported content directly inside Discord.

## ✨ How It Works

When a user posts an Instagram link:

```text
https://www.instagram.com/reel/Ddhz2L5x_KT/?stkn=ZWtyZ291NDBmeDM0
````

KK Instagram automatically:

1. Detects the Instagram URL
2. Removes unnecessary tracking parameters
3. Converts it to a `kkinstagram.com` URL
4. Deletes the original message
5. Reposts the transformed link while preserving the original sender's identity
6. Lets Discord generate an embeddable preview, making the Instagram content playable directly inside the server

```text
Instagram URL
      ↓
   KK Instagram
      ↓
Clean kkinstagram URL
      ↓
Discord Embed
      ↓
▶ Watch directly inside Discord
```

The result is a smoother experience for users who want to share Instagram content without forcing everyone to leave Discord and open Instagram.

## 🚀 Features

* 🔗 Automatic Instagram URL detection
* 🧹 Removes tracking/query parameters
* 🎬 Supports Instagram Reels
* 📺 Generates Discord-friendly embeds
* 👤 Preserves the original sender's name and avatar
* ✏️ Preserves surrounding message text
* 🔄 Supports multiple Instagram links in a single message
* 🤖 Ignores bot messages to prevent loops
* 🔐 Uses Discord's Message Content Intent
* ⚡ Lightweight Python implementation

## 🛠️ Tech Stack

* **Python**
* **discord.py**
* **Discord Gateway API**
* **Discord Webhooks**
* **python-dotenv**
* Regular expressions for URL detection and transformation

## 💻 Running the Bot

### 1. Create and activate a virtual environment

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your Discord bot token

Create a `.env` file in the project directory:

```env
DISCORD_TOKEN=your_bot_token_here
```

> ⚠️ Never commit your `.env` file or expose your bot token publicly.

### 4. Start the bot

```bash
python bot.py
```

Keep the process running for the bot to stay online.

## 🎯 Why?

Discord's native handling of Instagram links can be inconsistent, and users often have to leave the app to view shared content.

KK Instagram acts as a small bridge between Instagram and Discord, transforming supported links into URLs that Discord can embed and render directly in the conversation.

No commands are required. Just paste an Instagram link and let the bot handle the rest.

