import streamlit as st
from scrape import scrape, extract_only_content, clean, split_dom_content
from parse import parse_with_groq

# Streamlit App Title
st.title("The Ultimate Web Scraper 🚀")

# URL Input Field
url = st.text_input("Enter the URL to scrape (e.g., https://www.swiggy.com):")

# Scrape Button
if st.button("Scrape"):
    # Check if URL is provided
    if not url.strip():
        st.error("Please enter a valid URL.")
    else:
        st.write("Scraping the URL:", url)
        
        try:
            # Call the scraping function
            results = scrape(url)
            if results:
                st.success("Scraping completed successfully!")
                body_content = extract_only_content(results)
                cleaned_content = clean(body_content)

                st.session_state.dom_content = cleaned_content

                with st.expander("View DOM Content"):
                    st.text_area("Dom Content", cleaned_content, height=300)
                
            else:
                st.warning("No results were returned from the scrape.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        
if "dom_content" in st.session_state:
    parse_description = st.text_input("Describe what you would like to pass (e.g., 'Suggest me a product')")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content 🤔")
            dom_chunks = split_dom_content(st.session_state.dom_content)
            results = parse_with_groq(dom_chunks, parse_description)
            st.write(results)
