import pytest
from utils.nlp_processor import NLPProcessor
from utils.file_handler import FileHandler
from utils.dictionary import Dictionary
import os

class TestNLPProcessor:
    def setup_method(self):
        self.processor = NLPProcessor()
    
    def test_spell_checking(self):
        text = "Thiss is a testt"
        errors = self.processor.check_spelling(text)
        assert len(errors) > 0
        assert any(error["word"] == "Thiss" for error in errors)
    
    def test_get_suggestions(self):
        suggestions = self.processor.get_suggestions("teh")
        assert len(suggestions) > 0
        assert "the" in suggestions or "ten" in suggestions
    
    def test_grammar_checking(self):
        text = "this is a sentence. another sentence"
        errors = self.processor.check_grammar(text)
        assert len(errors) > 0
        # Should detect missing capital at start
    
    def test_word_count(self):
        text = "This is a test sentence"
        count = self.processor.get_word_count(text)
        assert count == 5
    
    def test_sentence_count(self):
        text = "First sentence. Second sentence. Third sentence."
        count = self.processor.get_sentence_count(text)
        assert count == 3
    
    def test_readability_score(self):
        text = "This is a test. It has multiple sentences. They are short."
        score = self.processor.get_readability_score(text)
        assert "words_per_sentence" in score
        assert "avg_word_length" in score
        assert score["total_sentences"] == 3

class TestDictionary:
    def setup_method(self):
        self.dictionary = Dictionary()
    
    def test_add_word(self):
        self.dictionary.add_word("customword")
        assert self.dictionary.is_valid_word("customword")
    
    def test_remove_word(self):
        self.dictionary.add_word("removeword")
        assert self.dictionary.is_valid_word("removeword")
        self.dictionary.remove_word("removeword")
        assert not self.dictionary.is_valid_word("removeword")
    
    def test_ignore_word(self):
        self.dictionary.ignore_word("ignoreme")
        assert self.dictionary.is_valid_word("ignoreme")
    
    def test_save_and_load_custom_dictionary(self):
        self.dictionary.add_word("testword")
        self.dictionary.save_custom_dictionary("test_dict.json")
        
        new_dict = Dictionary()
        new_dict.load_custom_dictionary("test_dict.json")
        assert new_dict.is_valid_word("testword")
        
        # Cleanup
        if os.path.exists("test_dict.json"):
            os.remove("test_dict.json")

class TestFileHandler:
    def test_get_file_info_nonexistent(self):
        info = FileHandler.get_file_info("nonexistent.txt")
        assert info is None

# Run tests with: pytest tests/test_utils.py -v
