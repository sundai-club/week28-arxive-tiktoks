import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment
API_KEY = os.getenv('OPENAI_API_KEY')

def setup_webdriver():
    """Setup Selenium WebDriver with Chrome options."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)

def scrape_arxiv_links(category):
    """Scrapes all arxiv links from a given category using Selenium and BeautifulSoup."""
    url_dict = {
        'CVPR': 'https://trendingpapers.com/papers?o=pagerank_growth&pd=24%20hours&cc=Cited%20and%20uncited%20papers&c=Computer%20Science%20-%20Computer%20Vision%20and%20Pattern%20Recognition',
        'ML': 'https://trendingpapers.com/papers?o=pagerank_growth&pd=24%20hours&cc=Cited%20and%20uncited%20papers&c=Computer%20Science%20-%20Machine%20Learning',
        'CL': 'https://trendingpapers.com/papers?o=pagerank_growth&pd=24%20hours&cc=Cited%20and%20uncited%20papers&c=Computer%20Science%20-%20Computation%20and%20Language',
        'IT': 'https://trendingpapers.com/papers?o=pagerank_growth&pd=24%20hours&cc=Cited%20and%20uncited%20papers&c=Computer%20Science%20-%20Information%20Theory',
        'Robotics': 'https://trendingpapers.com/papers?o=pagerank_growth&pd=24%20hours&cc=Cited%20and%20uncited%20papers&c=Computer%20Science%20-%20Robotics',
        'Crypto': 'https://trendingpapers.com/papers?o=pagerank_growth&pd=24%20hours&cc=Cited%20and%20uncited%20papers&c=Computer%20Science%20-%20Cryptography%20and%20Security',
        'AI': 'https://trendingpapers.com/papers?o=pagerank_growth&pd=24%20hours&cc=Cited%20and%20uncited%20papers&c=Computer%20Science%20-%20Artificial%20Intelligence'
    }

    driver = setup_webdriver()
    url = url_dict.get(category)
    if not url:
        print("Invalid category. Please choose from the following:", list(url_dict.keys()))
        return []

    driver.get(url)
    time.sleep(10)  # Allow time for the page to load
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'lxml')
    arxiv_links = [link['href'] for link in soup.find_all('a', href=True) if 'arxiv.org/abs/' in link['href']]
    driver.quit()
    return arxiv_links  # Return links as a list

import argparse

def main():
    parser = argparse.ArgumentParser(description='Scrape arXiv links for a given category.')
    parser.add_argument('category', 
                    nargs='?', 
                    choices=['CVPR', 'ML', 'CL', 'IT', 'Robotics', 'Crypto', 'AI'], 
                    default='CL', 
                    help='Category to scrape arXiv links for')
    args = parser.parse_args()

    scraped_links = scrape_arxiv_links(args.category)
    print(scraped_links)

if __name__ == "__main__":
    main()


# papers = extract_paper_titles(scraped_text)
# json_data = extract_json_from_string(papers)
# print(json_data)
# def extract_paper_titles(text):
#     """Extract paper titles using OpenAI's API."""
#     client = openai.OpenAI(api_key=API_KEY)
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "system", "content": "Extract only the links of academic papers from the following text. Give it back in a json with key 'links'"},
#             {"role": "user", "content": text}
#         ]
#     )
#     return response.choices[0].message.content

# def extract_json_from_string(input_string):
#     """Extracts JSON data from a string."""
#     start_index = input_string.find('{')
#     end_index = input_string.rfind('}') + 1  # Include the closing brace
    
#     if start_index == -1 or end_index == -1:
#         raise ValueError("No JSON data found in the text.")
    
#     json_str = input_string[start_index:end_index]
#     return json.loads(json_str)