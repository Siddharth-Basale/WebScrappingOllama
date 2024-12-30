import asyncio
import threading
import queue
from pyppeteer import launch
from bs4 import BeautifulSoup
import time
import streamlit as st

def scrape_with_pyppeteer(url, result_queue):
    """Scrapes the website using Pyppeteer (Headless Chrome) in a separate thread."""
    async def fetch():
        try:
            browser = await launch(headless=True)
            page = await browser.newPage()
            await page.goto(url)
            content = await page.content()
            await browser.close()
            result_queue.put(content)
        except Exception as e:
            result_queue.put(str(e))

    # Create and run the async task in a separate event loop within the thread
    loop = asyncio.new_event_loop()
    threading.Thread(target=loop.run_until_complete, args=(fetch(),)).start()

def scrape(url):
    """Main scraping function to call pyppeteer scraper."""
    try:
        result_queue = queue.Queue()  # Initialize the queue
        scrape_with_pyppeteer(url, result_queue)

        # Wait for the result (this could also be improved by making it async)
        content = result_queue.get()
        
        if isinstance(content, str) and "scraping failed" in content.lower():
            st.error(f"Scraping failed: {content}")
            return None
        
        if not content:
            st.error("Scraping returned empty content.")
            return None
        
        # Debugging: log the first 500 characters of the content
        st.write(f"Fetched content preview (first 500 characters): {content[:500]}")
        
        return content
    except Exception as e:
        st.error(f"Scraping failed: {str(e)}")
        return None

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
