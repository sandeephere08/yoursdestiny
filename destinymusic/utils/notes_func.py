from typing import Dict, Any
from pyrogram.types import Message

class NoteFillings:
    """Class to handle note text fillings with message data."""
    
    def __init__(self, message: Message, text: str):
        """Initialize with message and text.
        
        Args:
            message (Message): The message object
            text (str): The text to fill
        """
        self.message = message
        self.text = text
        
    def __str__(self) -> str:
        """Return filled text with message data.
        
        Returns:
            str: Filled text
        """
        text = self.text
        
        # Fill user data
        if self.message.from_user:
            text = text.replace("{first}", self.message.from_user.first_name)
            text = text.replace("{last}", self.message.from_user.last_name or "")
            text = text.replace("{fullname}", self.message.from_user.first_name + " " + (self.message.from_user.last_name or ""))
            text = text.replace("{username}", self.message.from_user.username or "")
            text = text.replace("{mention}", self.message.from_user.mention)
            text = text.replace("{id}", str(self.message.from_user.id))
            
        # Fill chat data
        if self.message.chat:
            text = text.replace("{chatname}", self.message.chat.title or "")
            text = text.replace("{chatid}", str(self.message.chat.id))
            
        return text 