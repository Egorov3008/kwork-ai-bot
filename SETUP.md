# Setup Guide for Kwork AI Bot

## 🚀 Quick Start

### Step 1: Clone repository

```bash
git clone https://github.com/Egorov3008/kwork-ai-bot.git
cd kwork-ai-bot
```

### Step 2: Install dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Create environment file

```bash
cp .env.example .env
vim .env
```

Edit `.env` with your credentials:
```
BOT_TOKEN=your_telegram_bot_token
KWORK_USERNAME=your_kwork_username
KWORK_PASSWORD=your_kwork_password
AI_API_KEY=your_openrouter_api_key
CHECK_INTERVAL=1800
```

### Step 4: Get Telegram Bot Token

1. Open **@BotFather** in Telegram
2. Send `/newbot`
3. Follow instructions to create bot
4. Copy the token to `.env`

### Step 5: Get OpenRouter API Key

1. Go to https://openrouter.ai/
2. Sign up / Log in
3. Go to Settings → API Keys
4. Create new API key
5. Copy to `.env`

### Step 6: Run the bot

```bash
python main.py
```

### Step 7: Test the bot

In Telegram, open your bot and send:
- `/start` - Start the bot
- `/orders` - List active orders
- `/stats` - Show statistics

## 🔑 Required Credentials

### 1. Telegram Bot Token
- From **@BotFather**
- Format: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

### 2. Kwork Credentials
- Your Kwork username
- Your Kwork password
- Required for order monitoring

### 3. OpenRouter API Key
- From https://openrouter.ai/
- Used for AI response generation
- Cost: ~$0.0002 per request

## 📊 Bot Features

- **Automatic Monitoring**: Checks for new orders every 30 minutes
- **AI Responses**: Generates human-like responses using Qwen3.5
- **Real-time Notifications**: Instant alerts for new orders
- **Order Filtering**: Filter by keywords (Python, bots, etc.)
- **Editable Responses**: Edit AI responses before sending
- **Statistics**: Track orders, responses, and performance

## ⚙️ Configuration Options

### Check Interval
```
CHECK_INTERVAL=1800  # 30 minutes (default)
```

### AI Model
Edit `ai/generator.py` to change model:
```python
model = "openrouter/qwen/qwen3.5-35b-a3b"  # Default
# Or try other models:
# model = "openrouter/deepseek/deepseek-v3.2"  # Backup
# model = "openrouter/openai/gpt-4o"  # Premium
```

### Keywords Filter
Edit `config.py`:
```python
KEYWORDS = ["python", "bot", "telegram", "api"]
```

## 🐛 Troubleshooting

### Bot won't start
```bash
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### "Module not found" error
```bash
source venv/bin/activate
pip install pyrogram kwork openai aiosqlite python-dotenv
```

### Token invalid
- Check your bot token from @BotFather
- Ensure `.env` file has correct token
- Restart the bot

### No orders found
- Check if Kwork credentials are correct
- Verify Kwork account is active
- Check monitoring channels in config

### AI not generating responses
- Check OpenRouter API key
- Verify API key has enough balance
- Check network connection

## 📝 Next Steps

1. ✅ Install dependencies
2. ✅ Configure `.env` file
3. ✅ Run `python main.py`
4. ✅ Test with `/start` command
5. ✅ Monitor orders in Telegram
6. ✅ Review AI responses before sending

## 💡 Tips

- **Start small**: Test with 1-2 users first
- **Monitor costs**: AI requests cost ~$0.0002 each
- **Customize responses**: Edit AI templates in `ai/generator.py`
- **Set intervals**: Adjust `CHECK_INTERVAL` based on needs
- **Backup database**: Regularly backup `kwork_bot.db`

## 🔒 Security

- Never commit `.env` file to git
- Store API keys securely
- Use strong passwords for Kwork
- Monitor API usage and costs
- Regular backup of database

## 📚 Documentation

- [Pyrogram Documentation](https://docs.pyrogram.ai/)
- [OpenRouter Documentation](https://openrouter.ai/docs)
- [Kwork API](https://kwork.ru/api)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

---

**Need help?** Check GitHub issues or contact support.
