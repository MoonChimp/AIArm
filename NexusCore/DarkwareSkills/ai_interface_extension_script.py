```python
import requests
from bs4 import BeautifulSoup

def search(query):
    """
    Search for information on a given query using the Google Custom Search API.
    
    :param query: The search query to use.
    :type query: str
    
    :return: A list of relevant search results.
    :rtype: list
    
    :raises requests.exceptions.RequestException: If an error occurs while making the request.
    """
    # Set up the API endpoint and parameters
    api_key = 'YOUR_API_KEY'
    cx = 'YOUR_CX_ID'
    url = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={query}'
    
    try:
        # Make the request to the API
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse the response using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract relevant information from the search results
        results = []
        for item in soup.find_all('item'):
            title = item.find('title').text
            link = item.find('link').text
            snippet = item.find('snippet').text
            results.append({'title': title, 'link': link, 'snippet': snippet})
        
        return results
    
    except requests.exceptions.RequestException as e:
        raise e

# Example usage
if __name__ == '__main__':
    query = 'Python programming'
    try:
        results = search(query)
        for result in results:
            print(result['title'])
            print(result['link'])
            print(result['snippet'])
            print()
    except Exception as e:
        print(f'An error occurred: {e}')
```

This script defines a `search` function that takes a search query as input and returns a list of relevant search results using the Google Custom Search API. It includes error handling to catch any exceptions that may occur while making the request or parsing the response. The function is designed to be reusable, with clear docstrings explaining its purpose and parameters. Usage examples are provided in comments at the bottom of the file.