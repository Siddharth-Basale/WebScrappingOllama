import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from the .env file
load_dotenv()

# Get the API key from environment variables
API_KEY = os.getenv("GROQ_API_KEY")

# Check if API key is loaded successfully
if not API_KEY:
    raise ValueError(
        "API key not found. Please set GROQ_API_KEY in the .env file.")

# Template for instruction on extracting data
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response, also if you felt the need to add a tabel for good viewing,then give responce in tabel format. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

# Function to interact with the Groq API


def parse_with_groq(dom_chunks, parse_description):
    # Initialize the Groq client with API key
    client = Groq(api_key=API_KEY)  # Pass the API key here

    parsed_results = []

    # Iterate through chunks and send them to the Groq API
    for i, chunk in enumerate(dom_chunks, start=1):
        prompt = template.format(
            dom_content=chunk, parse_description=parse_description)

        # Send request to the Groq API using the formatted prompt
        completion = client.chat.completions.create(
            model="llama3-8b-8192",  # Groq model choice
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        # Handle streaming response
        response = ""
        for chunk in completion:
            response += chunk.choices[0].delta.content or ""

        # Append parsed result to the results list
        print(f"parsed batches {i} of {len(dom_chunks)}")
        parsed_results.append(response.strip())

    return "\n".join(parsed_results)


# Example usage (replace with actual DOM content and parse description)
# Replace with actual content
dom_chunks = ["chunk1 of content", "chunk2 of content"]
parse_description = "Extract key points from the content."

# Call the function to parse using Groq API
parsed_data = parse_with_groq(dom_chunks, parse_description)
print(parsed_data)
