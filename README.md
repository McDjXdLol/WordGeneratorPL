# WordGeneratorPL

A multithreaded Python script for generating valid Polish words using a dictionary trie and morphological analysis.

---

## Features

- Generates Polish words randomly using the full Polish alphabet.
- Ensures words pass morphological analysis with `morfeusz2`.
- Filters out rejected words and avoids words with unnatural letter patterns.
- Uses multithreading for faster word generation.
- Displays live progress with a terminal progress bar (`tqdm`) and colorful output.
- Highly customizable: set minimum words and minimum letters in the word.

---

## Requirements

Install the dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

Dependencies include:

- `marisa_trie`

- `morfeusz2`

- `tqdm`

## Usage
```bash
python word_hunt.py <min_words_to_generate> <min_letters_in_word>
```
Example:
```bash
python word_hunt.py 50 4
```
This generates 50 Polish words, each with at leasts 4 letters.

## Output

The script prints live updates for each thread:

- Found word (magenta and bold)

- Progress: number of words found

- Number of retries

- Time taken at the end

Example output:
```less
[Thread-1] Found word: kot
[Thread-1] Progress:  1/50 words found
[Thread-1] Retries: 15
Time taken: 2.34 sec
Found words: ['kot', 'pies', 'dom', ...]
```

## How it works

1. Loads Polish words from PL.txt into a trie for fast lookup.

2. Loads rejected words from rejected.txt.

3. Generates random words using the Polish alphabet.

4. Checks each word with morfeusz2 for valid morphological forms.

5. Uses threading to parallelize word generation.

6. Stops when the minimum number of words is reached.

## Notes

- Make sure PL.txt and rejected.txt are in the same folder as the script.

- Avoid setting min_letters_in_word below 3; words shorter than 3 letters are ignored.

- The script uses colorful terminal output—best viewed in terminals that support ANSI escape codes.

## License

More about [LICENSE](LICENSE)
