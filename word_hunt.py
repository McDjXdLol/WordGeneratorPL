import marisa_trie
import random
import threading
import time
from tqdm import tqdm
import morfeusz2
import re
import sys

RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"

# Dictionary
morf = morfeusz2.Morfeusz()

# Load Polish words
with open('PL.txt', encoding='utf-8') as f:
    words = [line.strip() for line in f]

trie = marisa_trie.Trie(words)

# Wczytaj słowa odrzucone do setu
with open('rejected.txt', encoding='utf-8') as f:
    odrzucone = set(line.strip() for line in f)

polish_alphabet = [
    "a","ą","b","c","ć","d","e","ę","f","g","h","i","j","k","l",
    "ł","m","n","ń","o","ó","p","q","r","s","ś","t","u","v","w",
    "x","y","z","ź","ż"
]

found_words = []
found_event = threading.Event()
lock = threading.Lock()
divide = 3  # liczba wątków

if len(sys.argv) <= 1:
    print("Usage: word_hunt.py <min_words_to_generate> <min_letters_in_word>")
    sys.exit(1)

try:
    MIN_WORDS = int(sys.argv[1])
    MIN_LETTERS = int(sys.argv[2])
    if MIN_WORDS <= 0:
        print("Oh... less than 1... heh 💁‍♂️ done 👍")
        sys.exit(1)
    if MIN_LETTERS <= 2:
        print("There is now words shorter that 3 letters!")
        raise ValueError
except ValueError:
    print("Usage: word_hunt.py <min_words_to_generate> <min_letters_in_word>")
    sys.exit(1)

tries = 0

# Pasek postępu
pbar = tqdm(total=0, bar_format="Tries: {n} | Time elapsed: {elapsed}")

def word_hunt(thread_name):
    global tries
    while not found_event.is_set():
        word = random.choice(polish_alphabet)
        while True:
            with lock:
                tries += 1
                pbar.n = tries
                pbar.refresh()
            word += random.choice(polish_alphabet)
            if word in trie:
                if word in odrzucone:
                    break  # słowo odrzucone, skip
                if not re.search(r"[aeiouyąęó]", word.lower()):
                    break
                if re.search(r"[^aeiouyąęó]{4,}", word):
                    break
                if len(word) < MIN_LETTERS:
                    break
                with lock:
                    if morf.analyse(word):
                        found_words.append(word)
                        print(f"\n[{CYAN}{thread_name}{RESET}] {GREEN}Found word:{RESET} {BOLD}{MAGENTA}{word}{RESET}")
                        print(f"[{CYAN}{thread_name}{RESET}] {GREEN}Progress:{RESET} {len(found_words):>3}/{MIN_WORDS} words found")
                        print(f"[{CYAN}{thread_name}{RESET}] {GREEN}Retries:{RESET} {YELLOW}{tries}{RESET}")
                        if len(found_words) >= MIN_WORDS:
                            found_event.set()  # zatrzymuje wszystkie wątki
                            return
            if len(word) > 32:
                break

threads = []
start_time = time.time()

for i in range(divide):
    t = threading.Thread(target=word_hunt, args=(f"Thread-{i+1}",))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

pbar.close()
end_time = time.time()
print(f"{GREEN}Time taken:{RESET} {BOLD}{YELLOW}{end_time - start_time:.2f} sec{RESET}")
print(f"{GREEN}Found words:{RESET} {BOLD}{MAGENTA}{found_words}{RESET}")
