import webbrowser

# Specify Microsoft Edge browser path (Windows default location)
edge_path = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
webbrowser.register('edge', None, webbrowser.BackgroundBrowser(edge_path))

# Open Google in Microsoft Edge
url = "https://www.google.com"
webbrowser.get('edge').open(url)