import streamlit as st
from playwright.sync_api import sync_playwright
from scrape import scrape, extract_only_content, clean, split_dom_content
from parse import parse_with_groq

# Streamlit App Title
st.title("The Ultimate Web Scraper 🚀")

# URL Input Field
url = st.text_input("Enter the URL to scrape (Enter complete URL, for eg: https://www.swiggy.com):")

# Scrape Button
if st.button("Scrape"):
    # Check if URL is provided
    if not url.strip():
        st.error("Please enter a valid URL.")
    else:
        st.write("Scraping the URL:", url)
        
        # Exception Handling for the Scrape Function
        try:
            # Use Playwright to handle headless browser scraping
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url)
                content = page.content()
                browser.close()

            # Proceed with scraping logic
            results = scrape(content)
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
            # Display error details in Streamlit
            st.error(f"An error occurred: {str(e)}")

        
if "dom_content" in st.session_state:
    parse_description = st.text_input(
        "Describe what you would like to pass (e.g., 'I am from Pune and I want to try something that I won't try regularly, suggest me.')")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content to ollama 🤔 ")
            dom_chunks = split_dom_content(st.session_state.dom_content)
            results = parse_with_groq(dom_chunks, parse_description)
            st.write(results)
