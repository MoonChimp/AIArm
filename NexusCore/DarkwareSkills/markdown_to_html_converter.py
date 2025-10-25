```python
import markdown

def markdown_to_html(markdown_text):
    """
    Converts Markdown formatted text to HTML format.
    
    Args:
        markdown_text (str): The Markdown formatted text to convert.
        
    Returns:
        str: The converted HTML text.
        
    Raises:
        TypeError: If the input is not a string.
    """
    if not isinstance(markdown_text, str):
        raise TypeError("Input must be a string")
    
    return markdown.markdown(markdown_text)

# Usage example
markdown_text = "# Hello World\nThis is a *Markdown* formatted text."
html_text = markdown_to_html(markdown_text)
print(html_text)
```