import streamlit as st
import anthropic
from datetime import datetime, timedelta
import time

# Page configuration
st.set_page_config(
    page_title="English Learning Chat", 
    page_icon="🤖",
    layout="centered"
)

# Usage limits configuration
DAILY_MESSAGE_LIMIT = 50  # Messages per day per user
HOURLY_MESSAGE_LIMIT = 10  # Messages per hour per user
MAX_MESSAGE_LENGTH = 500  # Characters per message
RATE_LIMIT_SECONDS = 3    # Seconds between messages

def check_usage_limits():
    """Check if user has exceeded usage limits"""
    current_time = datetime.now()
    
    # Initialize session state for tracking
    if "usage_tracker" not in st.session_state:
        st.session_state.usage_tracker = {
            "daily_count": 0,
            "hourly_count": 0,
            "last_reset_day": current_time.date(),
            "last_reset_hour": current_time.hour,
            "last_message_time": None,
            "total_messages": 0
        }
    
    tracker = st.session_state.usage_tracker
    
    # Reset daily counter
    if tracker["last_reset_day"] != current_time.date():
        tracker["daily_count"] = 0
        tracker["last_reset_day"] = current_time.date()
    
    # Reset hourly counter
    if tracker["last_reset_hour"] != current_time.hour:
        tracker["hourly_count"] = 0
        tracker["last_reset_hour"] = current_time.hour
    
    # Check rate limiting (time between messages)
    if tracker["last_message_time"]:
        time_since_last = (current_time - tracker["last_message_time"]).total_seconds()
        if time_since_last < RATE_LIMIT_SECONDS:
            wait_time = RATE_LIMIT_SECONDS - time_since_last
            return False, f"Please wait {wait_time:.1f} seconds before sending another message."
    
    # Check daily limit
    if tracker["daily_count"] >= DAILY_MESSAGE_LIMIT:
        return False, f"Daily limit reached ({DAILY_MESSAGE_LIMIT} messages). Try again tomorrow!"
    
    # Check hourly limit
    if tracker["hourly_count"] >= HOURLY_MESSAGE_LIMIT:
        return False, f"Hourly limit reached ({HOURLY_MESSAGE_LIMIT} messages). Try again in an hour!"
    
    return True, "OK"

def increment_usage():
    """Increment usage counters"""
    tracker = st.session_state.usage_tracker
    tracker["daily_count"] += 1
    tracker["hourly_count"] += 1
    tracker["total_messages"] += 1
    tracker["last_message_time"] = datetime.now()

def display_usage_stats():
    """Display current usage statistics"""
    if "usage_tracker" not in st.session_state:
        return
    
    tracker = st.session_state.usage_tracker
    
    # Calculate remaining limits
    daily_remaining = DAILY_MESSAGE_LIMIT - tracker["daily_count"]
    hourly_remaining = HOURLY_MESSAGE_LIMIT - tracker["hourly_count"]
    
    # Display in sidebar
    with st.sidebar:
        st.header("📊 Usage Stats")
        
        # Daily usage
        daily_progress = tracker["daily_count"] / DAILY_MESSAGE_LIMIT
        st.metric("Today's Messages", f"{tracker['daily_count']}/{DAILY_MESSAGE_LIMIT}")
        st.progress(daily_progress)
        
        # Hourly usage
        hourly_progress = tracker["hourly_count"] / HOURLY_MESSAGE_LIMIT
        st.metric("This Hour", f"{tracker['hourly_count']}/{HOURLY_MESSAGE_LIMIT}")
        st.progress(hourly_progress)
        
        # Total messages
        st.metric("Total Messages", tracker["total_messages"])
        
        # Warnings
        if daily_remaining <= 5:
            st.warning(f"⚠️ Only {daily_remaining} messages left today!")
        
        if hourly_remaining <= 2:
            st.warning(f"⚠️ Only {hourly_remaining} messages left this hour!")

def setup_anthropic():
    """Setup Anthropic client with API key from Streamlit secrets"""
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
        if not api_key.startswith("sk-ant-"):
            st.error("❌ Invalid Anthropic API key format!")
            return None
        client = anthropic.Anthropic(api_key=api_key)
        return client
    except KeyError:
        st.error("❌ Anthropic API key not found in secrets!")
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
    """Get response from Claude with token limits"""
    try:
        # Prepare conversation history (limit to last 6 messages to save tokens)
        conversation_messages = []
        recent_messages = st.session_state.messages[-6:] if len(st.session_state.messages) > 6 else st.session_state.messages
        
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
        
        # Call Claude API with conservative limits
        response = client.messages.create(
            model="claude-3-haiku-20240307",  # Most cost-effective model
            max_tokens=200,  # Limit response length to save costs
            temperature=0.7,
            system="You are a helpful English teacher. Keep responses concise but helpful (under 200 words). Focus on the most important points.",
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
    st.markdown("**Practice English with AI assistance - Now with usage limits!**")
    
    # Setup Anthropic client
    client = setup_anthropic()
    if not client:
        st.stop()
    
    # Initialize chat
    initialize_chat()
    
    # Display usage statistics
    display_usage_stats()
    
    # Welcome message if no chat history
    if len(st.session_state.messages) == 0:
        with st.chat_message("assistant"):
            welcome_text = "Hello! I'm Claude, your English learning assistant. I can help you practice English efficiently. What would you like to learn today?"
            st.write(welcome_text)
            st.session_state.messages.append({
                "role": "assistant",
                "content": welcome_text
            })
    
    # Display chat history
    display_chat_history()
    
    # Chat input with validation
    if user_input := st.chat_input("Type your message here..."):
        
        # Check message length
        if len(user_input) > MAX_MESSAGE_LENGTH:
            st.error(f"❌ Message too long! Please keep it under {MAX_MESSAGE_LENGTH} characters. (Current: {len(user_input)})")
            return
        
        # Check usage limits
        can_send, limit_message = check_usage_limits()
        if not can_send:
            st.error(f"❌ {limit_message}")
            return
        
        # Increment usage counter
        increment_usage()
        
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
    
    # Sidebar controls
    with st.sidebar:
        st.header("🎛️ Chat Controls")
        
        if st.button("🗑️ Clear Conversation", type="secondary"):
            st.session_state.messages = []
            st.rerun()
        
        st.header("⚙️ Current Limits")
        st.markdown(f"""
        - **Daily messages:** {DAILY_MESSAGE_LIMIT}
        - **Hourly messages:** {HOURLY_MESSAGE_LIMIT}
        - **Max message length:** {MAX_MESSAGE_LENGTH} chars
        - **Rate limit:** {RATE_LIMIT_SECONDS} seconds between messages
        - **Response length:** ~200 words max
        """)
        
        st.header("💡 Tips to Save Usage")
        st.markdown("""
        - Ask specific, focused questions
        - Combine multiple questions in one message
        - Use clear, concise language
        - Review previous responses before asking again
        """)

if __name__ == "__main__":
    main()
