import streamlit as st
import openai
import random
import time

# Set page configuration
st.set_page_config(
    page_title="AI Prompt Generator",
    page_icon="🤖",
    layout="wide"
)

# App title and description
st.title("🤖 AI Prompt Generator")
st.markdown("Generate effective prompts for your AI projects using OpenAI's GPT models")

# Sidebar for API key and settings
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter your OpenAI API key", type="password")
    model = st.selectbox(
        "Select GPT model",
        ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"]
    )
    temperature = st.slider("Temperature (creativity)", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

# Main content area
col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("Prompt Requirements")
    
    prompt_type = st.selectbox(
        "What type of prompt do you need?",
        [
            "Creative Writing", 
            "Code Generation", 
            "Data Analysis", 
            "Educational Content", 
            "Marketing Copy", 
            "ChatBot Design",
            "Custom"
        ]
    )
    
    if prompt_type == "Custom":
        prompt_type_custom = st.text_input("Enter your custom prompt type")
    
    target_model = st.selectbox(
        "Target AI model",
        ["GPT-4", "GPT-3.5", "Claude", "DALL-E", "Midjourney", "Stable Diffusion", "Other"]
    )
    
    if target_model == "Other":
        target_model_custom = st.text_input("Enter your target model")
    
    complexity = st.select_slider(
        "Prompt complexity",
        options=["Simple", "Moderate", "Complex", "Advanced"]
    )
    
    details = st.text_area("Additional requirements or context", height=150)

with col2:
    st.subheader("Generated Prompt")
    
    # Function to generate prompt using OpenAI
    def generate_prompt():
        if not api_key:
            st.error("Please enter your OpenAI API key in the sidebar")
            return None
        
        # Configure OpenAI client
        client = openai.OpenAI(api_key=api_key)
        
        # Prepare the right prompt type
        actual_prompt_type = prompt_type_custom if prompt_type == "Custom" else prompt_type
        actual_target_model = target_model_custom if target_model == "Other" else target_model
        
        # Create the system message
        system_message = f"""You are an expert prompt engineer. 
        Create a highly effective prompt based on the following requirements:
        
        1. Prompt will be used for: {actual_prompt_type}
        2. Target AI model: {actual_target_model}
        3. Complexity level: {complexity}
        
        Focus on creating a prompt that follows best practices for prompt engineering including:
        - Clear instructions
        - Structured formatting
        - Appropriate constraints
        - Example outputs where helpful
        - Step-by-step guidance for the AI
        
        Return ONLY the prompt itself, without explanations, introductions or quotation marks."""
        
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"Additional context: {details if details else 'None provided'}"}
                ],
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return None

    # Generate button
    if st.button("Generate Prompt", type="primary"):
        with st.spinner("Generating your prompt..."):
            # Add a slight delay for better UX
            time.sleep(0.5)
            result = generate_prompt()
            
            if result:
                st.text_area("Your generated prompt:", value=result, height=400)
                st.success("Prompt generated successfully!")
                st.download_button(
                    label="Download Prompt",
                    data=result,
                    file_name="ai_prompt.txt",
                    mime="text/plain"
                )
                
                # Tips for using the prompt
                with st.expander("Tips for using this prompt"):
                    st.markdown("""
                    - Try adjusting the temperature for more creative or more deterministic results
                    - For complex tasks, break down the prompt into multiple steps
                    - Consider using system and user role separation when applicable
                    - Test your prompt with different variations to find what works best
                    """)
    else:
        st.info("Fill in your requirements and click 'Generate Prompt' to get started")

# Example prompts section
st.subheader("Example Prompt Templates")
examples = st.expander("Click to view example prompt templates")

with examples:
    example_tabs = st.tabs(["Creative", "Technical", "Educational", "Marketing"])
    
    with example_tabs[0]:
        st.markdown("""
        ### Creative Writing Prompt Template
        ```
        I want you to write a [GENRE] story about [SUBJECT]. The story should be [LENGTH] and include the following elements:
        
        - Character: [CHARACTER DESCRIPTION]
        - Setting: [SETTING DESCRIPTION]
        - Theme: [THEME]
        - Tone: [TONE]
        
        Use [STYLE] writing style and include vivid descriptions and engaging dialogue.
        ```
        """)
    
    with example_tabs[1]:
        st.markdown("""
        ### Technical Code Prompt Template
        ```
        I need you to help me write a [LANGUAGE] function that [FUNCTION PURPOSE].
        
        Requirements:
        - Input: [INPUT DESCRIPTION]
        - Output: [OUTPUT DESCRIPTION]
        - Edge cases to handle: [EDGE CASES]
        - Performance considerations: [PERFORMANCE REQUIREMENTS]
        
        Include comments explaining the code and provide an example usage.
        ```
        """)
        
    with example_tabs[2]:
        st.markdown("""
        ### Educational Content Template
        ```
        Create a lesson plan for teaching [SUBJECT] to [AUDIENCE].
        
        The lesson should include:
        1. Learning objectives: [OBJECTIVES]
        2. Key concepts to cover: [CONCEPTS]
        3. Activities: [ACTIVITY TYPES]
        4. Assessment method: [ASSESSMENT]
        
        The content should be [DIFFICULTY LEVEL] and take approximately [TIME] to complete.
        ```
        """)
        
    with example_tabs[3]:
        st.markdown("""
        ### Marketing Copy Template
        ```
        Write a compelling [TYPE OF CONTENT] for [PRODUCT/SERVICE] targeting [TARGET AUDIENCE].
        
        Key selling points to include:
        - [SELLING POINT 1]
        - [SELLING POINT 2]
        - [SELLING POINT 3]
        
        The tone should be [TONE] and include a strong call-to-action that emphasizes [BENEFIT].
        Keep the content [LENGTH] and optimize it for [PLATFORM/MEDIUM].
        ```
        """)

# Footer
st.divider()
st.markdown("Created with ❤️ using Streamlit and OpenAI API")