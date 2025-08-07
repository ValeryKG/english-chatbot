import streamlit as st
import anthropic

# Page configuration
st.set_page_config(
    page_title="English Learning Chat", 
    page_icon="🤖",
    layout="centered"
)

def setup_anthropic():
    """Setup Anthropic client with API key from Streamlit secrets"""
    try:
        # Get API key from Streamlit secrets
        api_key = st.secrets["ANTHROPIC_API_KEY"]
        
        # Validate the key format
        if not api_key.startswith("sk-ant-"):
            st.error("❌ Invalid Anthropic API key format!")
            return None
            
        # Create Anthropic client
        client = anthropic.Anthropic(api_key=api_key)
        return client
        
    except KeyError:
        st.error("❌ Anthropic API key not found in secrets!")
        st.info("Please add 'ANTHROPIC_API_KEY' to your Streamlit secrets")
        st.code("""
        # Add this to your Streamlit Cloud secrets:
        ANTHROPIC_API_KEY = "sk-ant-your-key-here"
        """)
        return None
    except Exception as e:
        st.error(f"❌ Error setting up Anthropic: {str(e)}")
        return None

def initialize_chat():
    """Initialize chat session state"""
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_history():
    """Display all messages in the chat"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

def get_claude_response(user_input, client):
    """Get response from Claude"""
    try:
        # Prepare conversation history for Claude
        conversation_messages = []
        
        # Add recent messages for context (last 8 messages)
        recent_messages = st.session_state.messages[-8:] if len(st.session_state.messages) > 8 else st.session_state.messages
        
        for msg in recent_messages:
            if msg["role"] in ["user", "assistant"]:
                conversation_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        # Add current user message
        conversation_messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Call Claude API
        response = client.messages.create(
            model="claude-3-haiku-20240307",  # Fast and cost-effective model
            max_tokens=400,
            temperature=0.7,
            system="You are a friendly and patient English teacher named Claude. Help students learn English through natural conversation. Provide corrections when needed, explain grammar concepts clearly, and encourage practice. Keep responses conversational and supportive.",
            messages=conversation_messages
        )
        
        return response.content[0].text
        
    except anthropic.APIError as e:
        return f"API Error: {str(e)}"
    except anthropic.RateLimitError:
        return "Rate limit reached. Please try again in a moment."
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

def main():
    """Main application function"""
    # Header
    st.title("🤖 English Learning with Claude")
    st.markdown("**Practice your English conversation skills with AI assistance!**")
    
    # Setup Anthropic client
    client = setup_anthropic()
    if not client:
        st.stop()
    
    # Success message
    st.success("✅ Connected to Claude AI")
    
    # Initialize chat
    initialize_chat()
    
    # Welcome message if no chat history
    if len(st.session_state.messages) == 0:
        with st.chat_message("assistant"):
            welcome_text = "Hello! I'm Claude, your English learning assistant. I can help you with:\n\n- Grammar questions\n- Conversation practice\n- Vocabulary building\n- Writing assistance\n- Pronunciation tips\n\nWhat would you like to practice today?"
            st.write(welcome_text)
            st.session_state.messages.append({
                "role": "assistant",
                "content": welcome_text
            })
    
    # Display chat history
    display_chat_history()
    
    # Chat input
    if user_input := st.chat_input("Type your message here..."):
        # Add user message to history
        st.session_state.messages.append({
            "role": "user", 
            "content": user_input
        })
        
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
        
        # Get and display Claude's response
        with st.chat_message("assistant"):
            with st.spinner("Claude is thinking..."):
                claude_response = get_claude_response(user_input, client)
            st.write(claude_response)
            
            # Add Claude's response to history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": claude_response
            })
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ Chat Controls")
        
        if st.button("🗑️ Clear Conversation", type="secondary"):
            st.session_state.messages = []
            st.rerun()
        
        if st.button("📝 New Topic", type="secondary"):
            # Keep only the last 2 messages for context
            if len(st.session_state.messages) > 2:
                st.session_state.messages = st.session_state.messages[-2:]
            st.rerun()
        
        st.header("💡 Learning Tips")
        st.markdown("""
        **Try asking:**
        - "Can you explain when to use 'a' vs 'an'?"
        - "Help me practice past tense"
        - "What's the difference between 'affect' and 'effect'?"
        - "Can you check my grammar in this sentence?"
        - "Let's have a conversation about travel"
        """)
        
        st.header("🔧 App Info")
        st.markdown(f"""
        **Model:** Claude 3 Haiku  
        **Messages:** {len(st.session_state.messages)}  
        **Status:** 🟢 Connected
        """)

if __name__ == "__main__":
    main()
