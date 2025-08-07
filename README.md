# English Learning Chatbot

A Streamlit-based chatbot application for English language learning, powered by OpenAI's GPT-3.5-turbo.

## Features

- 🤖 Interactive chat interface
- 📚 English learning assistance
- 💬 Conversation practice
- 📝 Grammar explanations
- 🎯 Vocabulary building

## Files Structure

```
english-chatbot/
├── app.py              # Main application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd english-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   
   Create a `.streamlit/secrets.toml` file in your project directory:
   ```toml
   OPENAI_API_KEY = "your-openai-api-key-here"
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

## Deployment on Streamlit Cloud

1. **Push your code to GitHub** (without any API keys in the code)

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select your repository and branch

3. **Add your API key securely:**
   - In your Streamlit Cloud app dashboard
   - Go to "Settings" → "Secrets"
   - Add your secrets in TOML format:
     ```toml
     OPENAI_API_KEY = "your-openai-api-key-here"
     ```

## Security Notes

- ✅ API keys are stored securely in Streamlit secrets
- ✅ No sensitive information in the codebase
- ✅ Safe to commit to public repositories
- ❌ Never hardcode API keys in your code

## Getting Your OpenAI API Key

1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the key (starts with `sk-`)
4. Add it to your Streamlit secrets (not your code!)

## Usage

1. Open the app
2. Start typing in the chat input
3. The AI will respond as an English teacher
4. Use the sidebar to clear chat or view tips

## Support

If you encounter any issues:
- Check that your API key is properly set in secrets
- Ensure you have sufficient OpenAI API credits
- Verify your internet connection

---

**Important:** Never commit API keys to your repository. Always use Streamlit secrets for secure key management.
