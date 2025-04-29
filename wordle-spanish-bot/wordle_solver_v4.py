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

    def update_feedback(self, guess, feedback):
        """
        guess: string of 5 letters guessed
        feedback: string of 5 characters representing feedback for each letter:
            'v' = green (correct letter and position)
            'a' = yellow (correct letter wrong position)
            'n' = black/gray (letter not in word)
        """
        for i, (g_char, f_char) in enumerate(zip(guess, feedback)):
            if f_char == 'v':
                self.correct_positions[i] = g_char
                self.guessed_letters.add(g_char)
            elif f_char == 'a':
                self.wrong_positions[i].add(g_char)
                self.guessed_letters.add(g_char)
            elif f_char == 'n':
                # Only add to excluded if not already confirmed in guessed_letters
                if g_char not in self.guessed_letters:
                    self.excluded_letters.add(g_char)
        self.filter_words()

    def get_feedback_pattern(self, guess, target):
        pattern = []
        target_chars = list(target)
        # First pass for greens
        for i in range(5):
            if guess[i] == target[i]:
                pattern.append('v')
                target_chars[i] = None
            else:
                pattern.append(None)
        # Second pass for yellows and blacks
        for i in range(5):
            if pattern[i] is None:
                if guess[i] in target_chars:
                    pattern[i] = 'a'
                    target_chars[target_chars.index(guess[i])] = None
                else:
                    pattern[i] = 'n'
        return ''.join(pattern)

    def calculate_entropy(self, guess):
        pattern_counts = {}
        for target in self.possible_words:
            pattern = self.get_feedback_pattern(guess, target)
            pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
        entropy = 0.0
        total = len(self.possible_words)
        for count in pattern_counts.values():
            p = count / total
            entropy -= p * math.log2(p)
        return entropy

    def suggest_guess(self):
        if not self.possible_words:
            return None
        max_entropy = -1
        best_word = None
        # For the first guess, limit to a smaller subset to speed up calculation
        if len(self.possible_words) == len(self.word_list):
            candidate_words = self.possible_words[:500]  # limit to first 500 words for performance
        else:
            candidate_words = self.possible_words  # Use filtered possible words for entropy calculation
        for word in candidate_words:
            entropy = self.calculate_entropy(word)
            if entropy > max_entropy:
                max_entropy = entropy
                best_word = word
        return best_word

def load_word_list(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        words = [word.lower() for word in content.split() if len(word) == 5]
    return words

def main():
    print("Bienvenido al bot para resolver Wordle en español.")
    while True:
        start_command = input("Escribe 'nueva partida' para comenzar: ").strip().lower()
        if start_command == "nueva partida":
            print("Iniciando nueva partida...")
            break
        else:
            print("Comando no reconocido. Por favor, escribe 'nueva partida' para comenzar.")

    word_list = load_word_list("wordle-spanish-bot/palabras wordle español.txt")
    solver = WordleSolver(word_list)

    round_num = 1
    while True:
        guess = solver.suggest_guess()
        if guess is None:
            print("No se encontraron palabras posibles con la información dada.")
            break
        print(f"Intento {round_num}: Sugiero la palabra '{guess.upper()}'")
        feedback = input("Introduce el feedback para cada letra (v=verde, a=amarillo, n=negro), o 'c' para cambiar palabra sugerida: ").strip().lower()
        if feedback == "c":
            # Remove current guess from possible words and suggest next
            if guess in solver.possible_words:
                solver.possible_words.remove(guess)
            continue
        if feedback == "vvvvv":
            print("¡Felicidades! La palabra ha sido adivinada.")
            break
        if len(feedback) != 5 or not all(c in 'van' for c in feedback):
            print("Feedback inválido. Por favor, introduce una cadena de 5 caracteres usando solo v, a, n.")
            continue
        solver.update_feedback(guess, feedback)
        round_num += 1

if __name__ == "__main__":
    main()
