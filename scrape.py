from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def scrape(website):
    print("Launching Playwright 🚀")

    try:
        # Launching Playwright browser
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # Set headless=True for no GUI
            page = browser.new_page()

            # Set custom user-agent to avoid blocking
            page.set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

            # Navigate to the website
            page.goto(website)

            # Wait for the page body to load
            page.wait_for_selector("body")

            # Get the page source
            page_source = page.content()

            # Log the first 500 characters of the page content for debugging
            print("Page content fetched (first 500 chars):", page_source[:500])

            # Close the browser
            browser.close()

            # Return the page source
            return page_source

    except Exception as e:
        print(f"An error occurred: {e}")
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
    
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    """Splits the DOM content into chunks of a specified maximum length."""
    if not dom_content:
        raise ValueError("DOM content is empty or None. Cannot split content.")
    
    return [
        dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)
    ]
