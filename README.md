# English Learning Chatbot with Claude

A Streamlit-based English learning chatbot powered by Anthropic's Claude AI.

## Features

- 🤖 Interactive chat with Claude AI
- 📚 English learning assistance
- 💬 Natural conversation practice
- 📝 Grammar explanations and corrections
- 🎯 Vocabulary building
- 🔄 Context-aware responses

## Quick Start

### Option 1: Deploy on Streamlit Cloud (Recommended)

1. **Fork or clone this repository**

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select this repository

3. **Add your Anthropic API key:**
   - In your Streamlit app dashboard
   - Go to "Settings" → "Secrets"
   - Add your key:
     ```toml
     ANTHROPIC_API_KEY = "sk-ant-your-actual-api-key-here"
     ```

### Option 2: Run Locally

1. **Clone and setup:**
   ```bash
   git clone <your-repo-url>
   cd english-learning-chatbot
   pip install -r requirements.txt
   ```

2. **Create secrets file:**
   ```bash
   mkdir .streamlit
   echo 'ANTHROPIC_API_KEY = "sk-ant-your-key-here"' > .streamlit/secrets.toml
   ```

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## Getting Your Anthropic API Key

1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Go to "API Keys" section
4. Create a new API key
5. Copy the key (starts with `sk-ant-`)

## Project Structure

```
english-learning-chatbot/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This documentation
└── .streamlit/
    └── secrets.toml   # API key (local only - not committed)
```

## Features in Detail

### Chat Interface
- Clean, intuitive chat interface
- Message history preservation
- Context-aware conversations

### Learning Tools
- Grammar explanations
- Vocabulary assistance
- Conversation practice
- Writing feedback
- Pronunciation guidance

### Controls
- Clear conversation
- Start new topics
- Message counter
- Connection status

## Security

- ✅ API keys stored securely in Streamlit secrets
- ✅ No sensitive data in code repository
- ✅ Safe for public GitHub repositories
- ❌ Never hardcode API keys

## Model Information

This app uses **Claude 3 Haiku**, which is:
- Fast and responsive
- Cost-effective
- Excellent for conversational AI
- Optimized for educational content

## Troubleshooting

### Common Issues:

1. **"API key not found"**
   - Ensure your key is added to Streamlit secrets
   - Check the key name is exactly `ANTHROPIC_API_KEY`

2. **"Invalid API key format"**
   - Anthropic keys start with `sk-ant-`
   - Make sure you copied the complete key

3. **"Rate limit reached"**
   - Wait a moment before trying again
   - Check your Anthropic usage limits

### Support

- [Anthropic Documentation](https://docs.anthropic.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## Contributing

Feel free to submit issues and pull requests to improve the application!

---

**Built with ❤️ using Streamlit and Claude AI**
