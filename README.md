# Telegram Kwork AI Bot

Telegram bot for automatically monitoring Kwork freelance orders and generating AI-powered responses.

## 🚀 Features

- ✅ Automatic monitoring of Kwork orders via Telegram channels
- ✅ AI-generated responses using Qwen3.5 (OpenRouter)
- ✅ Real-time notifications with order details
- ✅ SQLite database for order tracking
- ✅ Flexible filtering by keywords
- ✅ Editable response drafts before sending
- ✅ Statistics and analytics

## 📦 Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 🔐 Configuration

1. **Create `.env` file:**
```bash
cp .env.example .env
vim .env
```

2. **Fill in your credentials:**
```
# Telegram Bot Token (from @BotFather)
BOT_TOKEN=your_bot_token_here

# Kwork Credentials
KWORK_USERNAME=your_kwork_username
KWORK_PASSWORD=your_kwork_password

# OpenRouter AI API Key
AI_API_KEY=your_openrouter_api_key

# Check interval (seconds)
CHECK_INTERVAL=1800
```

3. **AI Configuration (optional):**
```bash
cp .env.ai .env.ai.local
```

## 🚀 Usage

### **1. Run the bot:**

```bash
python main.py
```

### **2. Test the bot:**

```bash
python simple_bot.py
```

### **3. Check status:**

```bash
python test_setup.py
```

## 📊 Commands

Once the bot is running, you can use these commands in Telegram:

- `/start` - Start the bot
- `/orders` - List active orders
- `/stats` - Show statistics
- `/stop` - Stop monitoring

## 🤖 AI Integration

The bot uses Qwen3.5 via OpenRouter to generate human-like responses to freelance orders:

```python
from ai.generator import generate_ai_response

draft = await generate_ai_response({
    "title": "Order title",
    "description": "Order details",
    "budget": 10000
})
```

## 📁 Project Structure

```
kwork-ai-bot/
├── ai/                    # AI modules
│   └── generator.py       # AI response generator
├── bot/                   # Bot modules
│   ├── keyboards.py       # Inline keyboards
│   ├── handlers.py        # Message handlers
│   └── states.py          # FSM states
├── database/              # Database modules
│   └── db.py              # SQLite database
├── kwork/                 # Kwork API client
│   └── client.py          # Kwork API integration
├── main.py                # Main entry point
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── SETUP.md               # Setup guide
├── .env.example           # Environment template
└── .gitignore             # Git ignore rules
```

## 🔒 Security

- ✅ `.env` file is NOT committed to git
- ✅ API keys stored in secure environment variables
- ✅ Database stored locally
- ✅ No sensitive data logged

## 🛠️ Development

### **Test changes:**

```bash
python test_run.py
```

### **Check dependencies:**

```bash
python test_setup.py
```

## 🐛 Troubleshooting

### "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Token invalid"
- Check your bot token from @BotFather
- Restart the bot after updating `.env`

### "Kwork API error"
- Verify Kwork credentials in `.env`
- Check internet connection
- Verify Kwork account status

## 📊 Database Schema

The bot uses SQLite with the following tables:
- `orders` - Active freelance orders
- `stats` - Statistics tracking
- `user_preferences` - User settings

## 🌐 API Integration

### **Kwork API**
- Library: `kwork` (PyPI)
- Monitor: Telegram channels for new orders
- Filter: By keywords (Python, bots, etc.)

### **OpenRouter AI**
- Model: `openrouter/qwen/qwen3.5-35b-a3b`
- Purpose: Generate human-like responses
- Cost: ~$0.0002 per request

## 📝 License

MIT License

## 👤 Author

Created for freelance order management and automation.

## 🔗 Links

- **GitHub**: https://github.com/Egorov3008/kwork-ai-bot
- **OpenRouter**: https://openrouter.ai/
- **Kwork**: https://kwork.ru/
- **Pyrogram**: https://docs.pyrogram.ai/
