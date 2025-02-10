# Anki Decks

A collection of Python scripts for generating Anki flashcard decks using the `genanki` library. Each script generates a specific type of deck for different learning purposes.

## Repository Structure

```
anki-decks/
├── base.py              # Abstract base class for deck generation
├── requirements.txt     # Python package dependencies
├── template.md          # LLM-friendly template for new deck scripts
└── ... various Python scripts that generate Anki decks
```

## Usage

1. Create virtual environment (Python 3.10.6):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install requirements: `pip install -r requirements.txt`
3. Use template.md with an LLM to generate your deck structure
4. Create your deck script inheriting from base.py
5. Run your script: `python your_deck_script.py`