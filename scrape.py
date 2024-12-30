import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import time
import streamlit as st

async def scrape_with_pyppeteer(url):
    """Scrapes the website using Pyppeteer (Headless Chrome) asynchronously."""
    try:
        browser = await launch(headless=True)
        page = await browser.newPage()

        # Wait for the page to load completely by checking for a key element
        await page.goto(url, {'waitUntil': 'networkidle0'})  # Wait until no network connections are active
        time.sleep(2)  # Adding a slight delay to ensure content is loaded

        # Get the page content
        content = await page.content()
        await browser.close()

        if not content:
            return "Scraping failed: No content found."
        return content

    except Exception as e:
        return f"Scraping failed: {str(e)}"

async def scrape(url):
    """Main scraping function to call pyppeteer scraper asynchronously."""
    content = await scrape_with_pyppeteer(url)

    if isinstance(content, str) and "scraping failed" in content.lower():
        st.error(f"Scraping failed: {content}")
        return None

    if not content:
        st.error("Scraping returned empty content.")
        return None

    # Debugging: log the first 500 characters of the content
    st.write(f"Fetched content preview (first 500 characters): {content[:500]}")
    
    return content

def extract_only_content(content):
    """Extracts the body content from an HTML document."""
    if not content:
        raise ValueError("Content is empty or None. Cannot extract body.")
    
    soup = BeautifulSoup(content, "html.parser")
    body = soup.body
    if body:
        return str(body)  # Convert to string for further processing
    return ""

def clean(body):
    """Cleans the body content by removing scripts, styles, and extra whitespace."""
    if not body:
        raise ValueError("Body content is empty or None. Cannot clean content.")
    
    soup = BeautifulSoup(body, "html.parser")

    # Remove script and style tags
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get cleaned text
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    
    if not cleaned_content:
        raise ValueError("Cleaned content is empty after cleaning.")
    
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    """Splits the DOM content into chunks of a specified maximum length."""
    if not dom_content:
        raise ValueError("DOM content is empty or None. Cannot split content.")
    
    # Split the content into chunks of max_length
    return [
        dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)
    ]
