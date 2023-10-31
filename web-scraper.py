""""
Description: Topic Challenge 7B Web Scraping
Author: Andy Soutcharith    
Date: 10/30/2023
Usage: Get colour names from the provided url using HTMLParser and print them out
"""

from html.parser import HTMLParser
import urllib.request


class ColourParser(HTMLParser):
    """Initialize the parser with necessary attributes"""

    def __init__(self):
        super().__init__()
        self.read_colour_name = False
        self.current_colour_name = None
        self.colours = {}

    def handle_starttag(self, tag, attrs):
        """Handle the start tag of an HTML element"""
        attrs = dict(attrs)

        # Detect the start of the colour name td using background-color in style attribute
        if tag == 'td' and 'style' in attrs and 'background-color' in attrs['style']:
            self.read_colour_name = True

        # Check if the tag is the link with hex value
        if tag == 'a' and self.current_colour_name is not None:
            self.colours[self.current_colour_name] = "#" + attrs['href'][1:]
            self.current_colour_name = None

    def handle_data(self, data):
        """Handle the text inside an Html element"""
        data = data.strip()
        if self.read_colour_name:
            self.current_colour_name = data
            self.read_colour_name = False


url = 'https://www.colorhexa.com/color-names'

# Fetch the HTML content of the webpage
with urllib.request.urlopen(url) as response:
    html = response.read().decode('utf-8')

colour_parser = ColourParser()

colour_parser.feed(html)

# Print the extracted colour names and hex values
for colour_name, hex_value in colour_parser.colours.items():
    print(f"{colour_name} {hex_value}")

print(f"Total colors: {len(colour_parser.colours)}")
