import streamlit as st
from llm_handler import LLMHandler
from database import Database
from entity_extractor import EntityExtractor

# Page configuration
st.set_page_config(
    page_title="FinanceBot - AI Financial Assistant",
    page_icon="💰",
    layout="wide"
)

# Initialize components
@st.cache_resource
def init_components():
    llm = LLMHandler()
    db = Database()
    extractor = EntityExtractor()
    return llm, db, extractor

llm, db, extractor = init_components()

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_details' not in st.session_state:
    st.session_state.user_details = db.get_user_details()

# Sidebar
with st.sidebar:
    st.title("💰 FinanceBot")
    st.markdown("Your AI Financial Assistant")
    st.divider()
    
    st.subheader("User Profile")
    user_details = st.session_state.user_details
    
    if user_details:
        st.success("✅ Profile Detected")
        st.write(f"**Name:** {user_details.get('name', 'Not provided')}")
        st.write(f"**Email:** {user_details.get('email', 'Not provided')}")
        st.write(f"**Phone:** {user_details.get('phone', 'Not provided')}")
    else:
        st.info("💡 Share your details in the chat to personalize your experience!")
    
    st.divider()
    
    if st.button("🔄 Clear Conversation"):
        st.session_state.messages = []
        llm.reset_conversation()
        st.rerun()
    
    st.divider()
    st.caption("Powered by Llama 3.1 (Local)")

# Main chat interface
st.title("💬 Chat with FinanceBot")
st.caption("Ask me anything about finance, investments, loans, savings, and more!")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask your financial question..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Extract entities from user message
    entities = extractor.extract_entities(prompt)
    
    # Save user details if found
    if entities['name'] or entities['email'] or entities['phone']:
        db.save_user_details(
            name=entities['name'],
            email=entities['email'],
            phone=entities['phone']
        )
        st.session_state.user_details = db.get_user_details()
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = llm.chat(prompt)
            st.markdown(response)
    
    # Add assistant response to chat
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Save conversation to database
    db.save_conversation(prompt, response, entities)
    
    # Show extracted info (for demo purposes)
    if entities['name'] or entities['email'] or entities['phone']:
        with st.expander("🔍 Extracted Information"):
            st.json(entities)
