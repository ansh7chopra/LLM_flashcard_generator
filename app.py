import streamlit as st
from utils.file_utils import extract_text_from_pdf, extract_text_from_txt
from utils.llm_utils import generate_flashcards
import json
import pandas as pd

st.set_page_config(page_title="Flashcard Generator", layout="wide")

st.title("📚 LLM-Powered Flashcard Generator")
st.markdown("Upload a file or paste text below to generate flashcards.")

# Upload Section
uploaded_file = st.file_uploader("Upload a .pdf or .txt file", type=["pdf", "txt"])

# Paste Input
user_text = st.text_area("Or paste your educational content here", height=300)

# Generate Flashcards
if st.button("Generate Flashcards"):
    final_text = ""

    # Handle file or text input
    if uploaded_file:
        file_type = uploaded_file.name.split(".")[-1]
        if file_type == "pdf":
            final_text = extract_text_from_pdf(uploaded_file)
        elif file_type == "txt":
            final_text = extract_text_from_txt(uploaded_file)
        else:
            st.error("Unsupported file type.")
            st.stop()
    elif user_text.strip():
        final_text = user_text.strip()
    else:
        st.error("Please upload a file or paste some content.")
        st.stop()

    # Preview input
    st.success("Text extracted successfully!")
    st.text_area("Extracted Text Preview", final_text[:2000], height=300)

    # Generate flashcards
    with st.spinner("Generating flashcards..."):
        flashcards = generate_flashcards(final_text)

    st.success(f"{len(flashcards)} Flashcards Generated!")

    flashcards_list = []

    # Display flashcards
    for i, card in enumerate(flashcards, start=1):
        st.markdown(f"### Flashcard {i}")
        question, answer = "", ""

        lines = card.strip().split("\n")
        for line in lines:
            if line.startswith("Q:"):
                question = line[2:].strip()
                st.markdown(f"**Q:** {question}")
            elif line.startswith("A:"):
                answer = line[2:].strip()
                st.markdown(f"**A:** {answer}")

        flashcards_list.append({"Question": question, "Answer": answer})
        st.markdown("---")

    # Export buttons
    if flashcards_list:
        col1, col2 = st.columns(2)

        with col1:
            json_data = json.dumps(flashcards_list, indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name="flashcards.json",
                mime="application/json"
            )

        with col2:
            csv_data = pd.DataFrame(flashcards_list).to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name="flashcards.csv",
                mime="text/csv"
            )
