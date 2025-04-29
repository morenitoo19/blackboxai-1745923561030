import re

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

    def suggest_guess(self):
        if not self.possible_words:
            return None
        # Improved strategy: score words by letter frequency and return highest scoring word
        letter_freq = {}
        for word in self.possible_words:
            unique_letters = set(word)
            for letter in unique_letters:
                letter_freq[letter] = letter_freq.get(letter, 0) + 1
        max_score = -1
        best_word = None
        for word in self.possible_words:
            score = sum(letter_freq.get(letter, 0) for letter in set(word))
            if score > max_score:
                max_score = score
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
