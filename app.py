import streamlit as st
from anthropic import Anthropic

# 1. Page Configuration and Styling
st.set_page_config(page_title="Careers Chatbot Demo", page_icon="💼", layout="centered")
st.title("Enterprise Corp Careers Assistant")
st.subheader("Talk to our AI to ask questions or submit your resume.")

# 2. Sidebar for Configuration
st.sidebar.header("AI Settings")
api_key = st.sidebar.text_input("Enter Anthropic API Key:", type="password")
st.sidebar.markdown("""
### Instructions:
1. Get a key from [Anthropic Console](https://claude.com).
2. Paste it above.
3. Chat with the bot and try uploading a resume!
""")

# 3. Initialize Conversation State
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Display Existing Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle File Upload (Resume Capture Simulation)
uploaded_file = st.file_input("Upload your Resume (PDF or DOCX)", type=["pdf", "docx"])
if uploaded_file and "file_logged" not in st.session_state:
    st.session_state.file_logged = True
    st.session_state.messages.append({"role": "user", "content": f"[Uploaded Resume: {uploaded_file.name}]"})
    with st.chat_message("user"):
        st.markdown(f"[Uploaded Resume: {uploaded_file.name}]")

# 6. Handle User Text Chat Input
if user_input := st.chat_input("Ask about benefits, culture, or type your application details..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 7. Call the Live Claude API
    if not api_key:
        with st.chat_message("assistant"):
            st.error("Please enter your Anthropic API Key in the sidebar to talk to the live AI.")
    else:
        try:
            client = Anthropic(api_key=api_key)
            
            system_prompt = (
                "You are an AI Talent Acquisition Assistant for Enterprise Corp. Your goal is to welcome candidates, "
                "answer their questions about benefits/culture, and guide them to provide their Name, Email, and upload "
                "their resume. Be professional, clear, and concise."
            )
            
            with st.chat_message("assistant"):
                with st.spinner("Claude is thinking..."):
                    response = client.messages.create(
                        model="claude-3-5-sonnet-latest",
                        max_tokens=600,
                        system=system_prompt,
                        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    )
                    reply = response.content[0].text
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"API Error: {str(e)}")
