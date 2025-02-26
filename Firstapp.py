import os
import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

def enhance_prompt(role, context, task):
    """Enhance the user input into a structured prompt."""
    enhanced_prompt = f"""
    You are {role}.
    Context: {context}
    Task: {task}
    
    Please structure your response as follows:
    1. **Clarify assumptions** before answering.
    2. **Provide a well-structured response** in bullet points or numbered format.
    3. **Ensure clarity and completeness** in your explanation.
    """
    return enhanced_prompt

def get_gpt_response(prompt):
    """Send the enhanced prompt to OpenAI and get the response."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("AI Prompt Enhancer")
    st.write("Enter your inputs below, and we'll refine your prompt for better results!")
    
    role = st.text_input("Role", placeholder="e.g., Data Scientist, Teacher, Marketer")
    context = st.text_area("Context", placeholder="Describe the background information.")
    task = st.text_area("Task", placeholder="Explain what needs to be done.")
    
    if st.button("Enhance Prompt"):
        if role and context and task:
            enhanced_prompt = enhance_prompt(role, context, task)
            st.subheader("Enhanced Prompt")
            st.code(enhanced_prompt, language="markdown")
            
            st.subheader("GPT Response")
            response = get_gpt_response(enhanced_prompt)
            st.write(response)
        else:
            st.warning("Please fill in all fields before enhancing the prompt.")

if __name__ == "__main__":
    main()
