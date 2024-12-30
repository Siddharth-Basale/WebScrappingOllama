from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def scrape(website):
    print("Launching Playwright 🚀")

    try:
        with sync_playwright() as p:
            # Launch headless browser
            browser = p.chromium.launch(headless=True)  # Set headless=True for no GUI
            page = browser.new_page()
            page.goto(website)

            # Wait for the body to load
            page.wait_for_selector("body")
            
            # Get page source
            page_source = page.content()
            browser.close()
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
