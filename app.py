import streamlit as st
import openai

# Page configuration
st.set_page_config(
    page_title="English Learning Chat", 
    page_icon="🤖",
    layout="centered"
)

def setup_openai():
    """Setup OpenAI client with API key from Streamlit secrets"""
    try:
        # Get API key from Streamlit secrets (NOT from code)
        api_key = st.secrets["OPENAI_API_KEY"]
        openai.api_key = api_key
        return True
    except KeyError:
        st.error("❌ Please configure your OpenAI API key in Streamlit secrets")
        st.info("Go to your Streamlit app settings and add your API key")
        return False
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def initialize_chat():
    """Initialize chat session state"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        welcome_msg = {
            "role": "assistant", 
            "content": "Hello! I'm your English learning assistant. How can I help you practice English today?"
        }
        st.session_state.messages.append(welcome_msg)

def display_chat_history():
    """Display all messages in the chat"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

def get_ai_response(user_input):
    """Get response from OpenAI"""
    try:
        # Prepare messages for API
        messages = [
            {
                "role": "system", 
                "content": "You are a helpful English teacher. Help students learn English through conversation, explanations, and corrections. Be encouraging and patient."
            }
        ]
        
        # Add conversation history (last 10 messages for context)
        recent_messages = st.session_state.messages[-10:]
        messages.extend(recent_messages)
        
        # Add current user input
        messages.append({"role": "user", "content": user_input})
        
        # Call OpenAI API
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

def main():
    """Main application function"""
    st.title("🤖 English Learning Chatbot")
    st.write("Practice your English with AI assistance!")
    
    # Setup OpenAI (this will check for API key in secrets)
    if not setup_openai():
        st.stop()
    
    # Initialize chat
    initialize_chat()
    
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
        
        # Get and display AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                ai_response = get_ai_response(user_input)
            st.write(ai_response)
            
            # Add AI response to history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": ai_response
            })
    
    # Sidebar with controls
    with st.sidebar:
        st.header("🎛️ Controls")
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
        
        st.header("💡 Tips")
        st.markdown("""
        - Ask grammar questions
        - Practice conversations  
        - Request explanations
        - Get writing help
        - Learn new vocabulary
        """)

if __name__ == "__main__":
    main()
