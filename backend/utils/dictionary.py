import os
import json
from typing import Set, List

class Dictionary:
    def __init__(self, dictionary_file: str = None):
        self.words = set()
        self.custom_words = set()
        self.ignored_words = set()
        
        if dictionary_file and os.path.exists(dictionary_file):
            self.load_dictionary(dictionary_file)
    
    def load_dictionary(self, filepath: str):
        """Load dictionary from file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip().lower()
                    if word:
                        self.words.add(word)
        except Exception as e:
            print(f"Error loading dictionary: {e}")
    
    def add_word(self, word: str):
        """Add word to custom dictionary"""
        self.custom_words.add(word.lower())
    
    def remove_word(self, word: str):
        """Remove word from custom dictionary"""
        word_lower = word.lower()
        if word_lower in self.custom_words:
            self.custom_words.remove(word_lower)
    
    def ignore_word(self, word: str):
        """Add word to ignored list (for current session)"""
        self.ignored_words.add(word.lower())
    
    def is_valid_word(self, word: str) -> bool:
        """Check if word is valid"""
        word_lower = word.lower()
        return (
            word_lower in self.words or
            word_lower in self.custom_words or
            word_lower in self.ignored_words
        )
    
    def save_custom_dictionary(self, filepath: str):
        """Save custom words to file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({
                    "custom_words": list(self.custom_words),
                    "ignored_words": list(self.ignored_words)
                }, f, indent=2)
        except Exception as e:
            print(f"Error saving custom dictionary: {e}")
    
    def load_custom_dictionary(self, filepath: str):
        """Load custom words from file"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.custom_words = set(data.get("custom_words", []))
                    self.ignored_words = set(data.get("ignored_words", []))
        except Exception as e:
            print(f"Error loading custom dictionary: {e}")
