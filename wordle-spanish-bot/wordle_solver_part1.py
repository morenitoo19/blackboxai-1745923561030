import re
import math

class WordleSolver:
    def __init__(self, word_list):
        self.word_list = word_list
        self.possible_words = word_list.copy()
        self.guessed_letters = set()
        self.correct_positions = [None] * 5
        self.wrong_positions = [set() for _ in range(5)]
        self.excluded_letters = set()

    def filter_words(self):
        filtered = []
        for word in self.possible_words:
            if self.is_word_possible(word):
                filtered.append(word)
        self.possible_words = filtered
        print(f"[DEBUG] Palabras posibles restantes: {len(self.possible_words)}")

    def is_word_possible(self, word):
        # Check correct positions
        for i, c in enumerate(self.correct_positions):
            if c is not None and word[i] != c:
                return False
        # Check wrong positions
        for i, wrong_set in enumerate(self.wrong_positions):
            if word[i] in wrong_set:
                return False
        # Check excluded letters
        for c in self.excluded_letters:
            if c in word:
                return False
        # Check guessed letters presence
        for c in self.guessed_letters:
            if c not in word and c not in self.excluded_letters:
                return False
        return True
