from abc import ABC, abstractmethod
from pathlib import Path

import genanki
import hashlib
from dataclasses import dataclass


@dataclass
class DeckMetadata:
    title: str
    tags: list[str]
    description: str
    version: str
    support_url: str = "https://github.com/thomasasfk/anki-decks"
    author: str = "thomasasfk"
    license: str = "MIT"

    def validate(self) -> bool:
        if len(self.title) > 60:
            raise ValueError("Title must be 60 characters or less")
        if not self.tags:
            raise ValueError("At least one tag is required")
        if not self.description:
            raise ValueError("Description is required")
        return True


class AnkiDeck(ABC):
    def __init__(self, metadata: DeckMetadata):
        self.metadata = metadata
        self.metadata.validate()
        self._model_id = self._generate_id("model")
        self._deck_id = self._generate_id("deck")
        self.media_files: list[str] = []

    def _generate_id(self, prefix: str) -> int:
        stable_input = f"{prefix}-{self.metadata.title}-{self.metadata.author}-{self.metadata.version}"
        hash_value = int(hashlib.md5(stable_input.encode()).hexdigest()[:8], 16)
        return hash_value % (2 ** 31)

    def _format_description(self) -> str:
        tags = ", ".join(self.metadata.tags)

        return f"""{self.metadata.title}

{self.metadata.description}

Deck Information:
Version: {self.metadata.version}
Author: {self.metadata.author} 
License: {self.metadata.license}
Tags: {tags}

Support:
For support, bug reports, or feature requests, please visit:
{self.metadata.support_url}"""

    @abstractmethod
    def create_model(self) -> genanki.Model:
        """Create and return the Anki model for the deck"""
        pass

    @abstractmethod
    def generate_cards(self) -> list[genanki.Note]:
        """Generate and return a list of Anki notes"""
        pass

    def get_default_css(self) -> str:
        return """
        .card {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: #1a1a1a;
            color: #ffffff;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
            font-size: 16px;
            line-height: 1.5;
        }
        .question {
            font-size: 1.2em;
            margin-bottom: 20px;
        }
        .answer {
            font-size: 1.1em;
            color: #4CAF50;
        }
        img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 10px 0;
        }
        .nightMode {
            background-color: #1a1a1a;
            color: #ffffff;
        }
        """

    def create_deck(self) -> genanki.Deck:
        deck = genanki.Deck(self._deck_id, self.metadata.title)
        deck.description = self._format_description()
        for note in self.generate_cards():
            deck.add_note(note)
        return deck

    def save_deck(self, output_filename: str) -> None:
        bin_path = Path(__file__).parent / 'bin'
        bin_path.mkdir(exist_ok=True)
        package = genanki.Package(self.create_deck())
        if self.media_files:
            package.media_files = self.media_files
        package.write_to_file(str(bin_path / output_filename))