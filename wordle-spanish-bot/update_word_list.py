def main():
    base_words_path = "wordle-spanish-bot/palabras wordle español.txt"
    spanish_words_path = "wordle-spanish-bot/spanish_words.txt"

    # Read base words
    with open(base_words_path, "r", encoding="utf-8") as f:
        base_words_content = f.read()
    base_words = set(base_words_content.split())

    # Read spanish words
    with open(spanish_words_path, "r", encoding="utf-8") as f:
        spanish_words = f.read().splitlines()

    # Filter 5-letter words (assuming uppercase) and not proper names (all uppercase)
    five_letter_words = set(word for word in spanish_words if len(word) == 5 and word.isupper())

    # Find missing words
    missing_words = five_letter_words - base_words

    if missing_words:
        print(f"Adding {len(missing_words)} missing words to base words list.")
        updated_words = base_words.union(missing_words)
        # Sort words alphabetically
        updated_words_sorted = sorted(updated_words)
        # Write back to base words file
        with open(base_words_path, "w", encoding="utf-8") as f:
            f.write(" ".join(updated_words_sorted))
        print("Base words list updated successfully.")
    else:
        print("No missing words to add.")

if __name__ == "__main__":
    main()
