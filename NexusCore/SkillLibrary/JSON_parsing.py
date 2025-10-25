```python
import json

def parse_json(json_string):
    """
    Parses a JSON string and returns a usable data structure.
    
    Args:
        json_string (str): The JSON string to be parsed.
        
    Returns:
        dict: A dictionary representing the parsed JSON data.
        
    Raises:
        ValueError: If the input JSON string is not valid.
    """
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON string: {e}")
```

This function takes a JSON string as input and uses Python's built-in `json` module to parse it into a dictionary. If the input string is not valid JSON, the function will raise a `ValueError` with an appropriate error message.

The function includes a docstring that explains its usage, including the arguments it accepts and the return value it produces. It also includes error handling using Python's built-in exception handling mechanism to catch any errors raised by the `json.loads()` method and raise a `ValueError` with a helpful error message if necessary.