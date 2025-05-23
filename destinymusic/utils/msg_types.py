import re
from typing import Tuple, List
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def button_markdown_parser(text: str) -> Tuple[str, List[List[InlineKeyboardButton]]]:
    """Parse markdown text and extract buttons.
    
    Args:
        text (str): Text containing markdown buttons
        
    Returns:
        Tuple[str, List[List[InlineKeyboardButton]]]: Parsed text and list of button rows
    """
    buttons = []
    text = text.strip()
    
    # Find all button patterns [text](url)
    button_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
    matches = re.finditer(button_pattern, text)
    
    for match in matches:
        button_text = match.group(1)
        button_url = match.group(2)
        buttons.append([InlineKeyboardButton(text=button_text, url=button_url)])
        
    # Remove button markdown from text
    text = re.sub(button_pattern, '', text).strip()
    
    return text, buttons 