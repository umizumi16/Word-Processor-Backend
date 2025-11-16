import nltk
from nltk.corpus import words
from nltk.tokenize import word_tokenize, sent_tokenize
import re
from typing import List, Dict, Tuple

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('words')

class NLPProcessor:
    def __init__(self):
        self.english_words = set(word.lower() for word in words.words())
        self.common_words = self._load_common_words()
    
    def _load_common_words(self) -> set:
        """Load commonly used words to reduce false positives"""
        common = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have',
            'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you',
            'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they',
            'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one',
            'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out',
            'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when',
            'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know',
            'take', 'people', 'into', 'year', 'your', 'good', 'some',
            'could', 'them', 'see', 'other', 'than', 'then', 'now',
            'look', 'only', 'come', 'its', 'over', 'think', 'also',
            'back', 'after', 'use', 'two', 'how', 'our', 'work',
            'first', 'well', 'way', 'even', 'new', 'want', 'because',
            'any', 'these', 'give', 'day', 'most', 'us'
        }
        return common
    
    def check_spelling(self, text: str) -> List[Dict]:
        """
        Check spelling in text
        Returns list of misspelled words with positions
        """
        # Tokenize into words
        words_in_text = word_tokenize(text)
        errors = []
        
        position = 0
        for word in words_in_text:
            # Find actual position in text
            word_pos = text.find(word, position)
            
            # Check if word is alphabetic and not a common word
            if word.isalpha() and len(word) > 1:
                word_lower = word.lower()
                
                if word_lower not in self.english_words and word_lower not in self.common_words:
                    errors.append({
                        "word": word,
                        "position": word_pos,
                        "length": len(word),
                        "suggestions": self.get_suggestions(word_lower)
                    })
            
            position = word_pos + len(word)
        
        return errors
    
    def get_suggestions(self, word: str, max_suggestions: int = 5) -> List[str]:
        """Generate spelling suggestions using edit distance"""
        suggestions = []
        word = word.lower()
        
        # Check words with same starting letter and similar length
        for dict_word in self.english_words:
            if dict_word[0] == word[0]:
                if abs(len(dict_word) - len(word)) <= 2:
                    distance = self._levenshtein_distance(word, dict_word)
                    if distance <= 2:
                        suggestions.append((dict_word, distance))
        
        # Sort by distance and return top suggestions
        suggestions.sort(key=lambda x: x[1])
        return [word for word, _ in suggestions[:max_suggestions]]
    
    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings"""
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def check_grammar(self, text: str) -> List[Dict]:
        """
        Basic grammar checking
        Returns list of grammar errors
        """
        errors = []
        sentences = sent_tokenize(text)
        
        position = 0
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            sent_pos = text.find(sentence, position)
            
            if sentence:
                # Check capitalization
                if not sentence[0].isupper():
                    errors.append({
                        "type": "capitalization",
                        "message": "Sentence should start with a capital letter",
                        "position": sent_pos,
                        "length": 1,
                        "sentence_index": i
                    })
                
                # Check ending punctuation
                if sentence[-1] not in '.!?':
                    errors.append({
                        "type": "punctuation",
                        "message": "Sentence should end with proper punctuation",
                        "position": sent_pos + len(sentence),
                        "length": 0,
                        "sentence_index": i
                    })
                
                # Check for double spaces
                if '  ' in sentence:
                    double_space_pos = sentence.find('  ')
                    errors.append({
                        "type": "spacing",
                        "message": "Multiple consecutive spaces detected",
                        "position": sent_pos + double_space_pos,
                        "length": 2,
                        "sentence_index": i
                    })
                
                # Check for repeated words
                words_list = sentence.split()
                for j in range(len(words_list) - 1):
                    if words_list[j].lower() == words_list[j + 1].lower():
                        errors.append({
                            "type": "repetition",
                            "message": f"Repeated word: '{words_list[j]}'",
                            "position": sent_pos + sentence.find(words_list[j]),
                            "length": len(words_list[j]) * 2 + 1,
                            "sentence_index": i
                        })
            
            position = sent_pos + len(sentence)
        
        return errors
    
    def get_word_count(self, text: str) -> int:
        """Get word count"""
        words_list = word_tokenize(text)
        return len([w for w in words_list if w.isalnum()])
    
    def get_sentence_count(self, text: str) -> int:
        """Get sentence count"""
        sentences = sent_tokenize(text)
        return len(sentences)
    
    def get_readability_score(self, text: str) -> Dict:
        """Calculate basic readability metrics"""
        words_list = word_tokenize(text)
        sentences = sent_tokenize(text)
        
        word_count = len([w for w in words_list if w.isalnum()])
        sentence_count = len(sentences)
        
        if sentence_count == 0:
            return {"words_per_sentence": 0, "avg_word_length": 0}
        
        words_per_sentence = word_count / sentence_count
        avg_word_length = sum(len(w) for w in words_list if w.isalnum()) / word_count if word_count > 0 else 0
        
        return {
            "words_per_sentence": round(words_per_sentence, 2),
            "avg_word_length": round(avg_word_length, 2),
            "total_words": word_count,
            "total_sentences": sentence_count
        }
