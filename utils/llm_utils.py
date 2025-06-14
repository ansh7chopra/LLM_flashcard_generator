from transformers import pipeline

flashcard_generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    max_length=256,
    do_sample=False
)

def split_text(text, chunk_size=300):
    words = text.split()
    return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def generate_flashcards(text):
    chunks = split_text(text, chunk_size=300)
    flashcards = []

    for chunk in chunks[:15]:  # Max 15 flashcards
        prompt = f"""
Create one flashcard from this text in the following format:

Q: [Your question]
A: [Your answer]

Text:
{chunk}
"""
        result = flashcard_generator(prompt)[0]['generated_text']

        # If format is missing, wrap the result manually
        if "Q:" not in result or "A:" not in result:
            result = f"Q: What is discussed in the text?\nA: {result.strip()}"

        flashcards.append(result.strip())

    return flashcards
