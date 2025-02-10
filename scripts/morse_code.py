from base import AnkiDeck, DeckMetadata
import genanki
from typing import Dict, List, Tuple
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine
import os
from pathlib import Path
from abc import ABC
import hashlib


class BaseMorseDeck(AnkiDeck, ABC):
    MORSE_CODE = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
        'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
        'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
        'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
        'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
        'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--',
        '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
        '9': '----.'
    }

    def __init__(self, metadata: DeckMetadata):
        super().__init__(metadata)
        self.dot_duration = 100  # milliseconds
        self.dash_duration = self.dot_duration * 3
        self.element_gap = self.dot_duration
        self.letter_gap = self.dot_duration * 3
        self.frequency = 800  # Hz
        self.audio_path = Path('media')
        self.audio_path.mkdir(exist_ok=True)
        self.generate_audio_files()

        # Generate a unique model ID based on the deck type
        self._model_id = self._generate_model_id()

    def _generate_model_id(self) -> int:
        """Generate a unique model ID based on the class name and base ID"""
        # Create a unique string combining the class name and base model ID
        unique_string = f"{self.__class__.__name__}_{self._model_id}"
        # Generate a hash of this string
        hash_object = hashlib.md5(unique_string.encode())
        # Convert first 8 digits of hash to integer
        return int(hash_object.hexdigest()[:8], 16)

    def get_custom_css(self) -> str:
        return super().get_default_css() + '''
            .card {
                background: transparent;
                border-radius: 12px;
                padding: 2em;
                max-width: 600px;
                margin: 20px auto;
            }

            .content {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 1.5em;
            }

            .character {
                font-size: 4em;
                font-weight: 600;
                color: #e0e0e0;
                font-family: 'Arial', sans-serif;
            }

            .morse {
                font-family: 'Courier New', monospace;
                font-size: 2.5em;
                color: #cccccc;
                letter-spacing: 0.1em;
            }

            .audio-controls {
                margin-top: 1em;
                padding: 0.75em 1.5em;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                display: inline-flex;
                align-items: center;
                gap: 0.5em;
            }

            hr {
                border: none;
                height: 2px;
                background: rgba(255, 255, 255, 0.2);
                margin: 1.5em 0;
                width: 100%;
            }

            .answer {
                font-size: 2em;
                color: #e0e0e0;
                text-align: center;
            }
        '''

    def generate_morse_audio(self, morse_code: str) -> AudioSegment:
        audio = AudioSegment.empty()

        for symbol in morse_code:
            if symbol == '.':
                tone = Sine(self.frequency).to_audio_segment(duration=self.dot_duration)
            elif symbol == '-':
                tone = Sine(self.frequency).to_audio_segment(duration=self.dash_duration)

            audio += tone
            audio += AudioSegment.silent(duration=self.element_gap)

        return audio

    def generate_audio_files(self) -> None:
        for char, morse in self.MORSE_CODE.items():
            filename = f'morse_{char}.mp3'
            filepath = self.audio_path / filename

            if not filepath.exists():  # Only generate if file doesn't exist
                audio = self.generate_morse_audio(morse)
                audio.export(str(filepath), format='mp3')

            self.media_files.append(str(filepath))

    def cleanup_media(self) -> None:
        for file in self.media_files:
            try:
                os.remove(file)
            except OSError as e:
                print(f"Error deleting {file}: {e}")
        try:
            self.audio_path.rmdir()
        except OSError as e:
            print(f"Error removing media directory: {e}")

    def _generate_note_id(self, char: str) -> int:
        """Generate a unique note ID based on the character and deck type"""
        # Combine class name, character, and a salt for uniqueness
        unique_string = f"{self.__class__.__name__}_{char}_{self._model_id}"
        hash_object = hashlib.md5(unique_string.encode())
        # Use first 8 digits of hash as note ID
        return int(hash_object.hexdigest()[:8], 16)


class VisualToMorseDeck(BaseMorseDeck):
    def create_model(self) -> genanki.Model:
        return genanki.Model(
            self._model_id,
            'Visual to Morse Model',
            fields=[
                {'name': 'Character'},
                {'name': 'MorseCode'},
                {'name': 'Audio'}
            ],
            templates=[{
                'name': 'Visual to Morse',
                'qfmt': '''
                    <div class="content">
                        <div class="character">{{Character}}</div>
                    </div>
                ''',
                'afmt': '''
                    {{FrontSide}}
                    <hr>
                    <div class="content">
                        <div class="morse">{{MorseCode}}</div>
                        <div class="audio-controls">{{Audio}}</div>
                    </div>
                '''
            }],
            css=self.get_custom_css()
        )

    def generate_cards(self) -> list[genanki.Note]:
        model = self.create_model()
        notes = []

        for char, morse in self.MORSE_CODE.items():
            audio_tag = f'[sound:morse_{char}.mp3]'
            note = genanki.Note(
                model=model,
                fields=[char, morse, audio_tag],
                guid=self._generate_note_id(char),
                tags=self.metadata.tags + ['visual-to-morse']
            )
            notes.append(note)

        return notes


class MorseToVisualDeck(BaseMorseDeck):
    def create_model(self) -> genanki.Model:
        return genanki.Model(
            self._model_id,
            'Morse to Visual Model',
            fields=[
                {'name': 'Character'},
                {'name': 'MorseCode'},
                {'name': 'Audio'}
            ],
            templates=[{
                'name': 'Morse to Character',
                'qfmt': '''
                    <div class="content">
                        <div class="morse">{{MorseCode}}</div>
                    </div>
                ''',
                'afmt': '''
                    {{FrontSide}}
                    <hr>
                    <div class="content">
                        <div class="character">{{Character}}</div>
                        <div class="audio-controls">{{Audio}}</div>
                    </div>
                '''
            }],
            css=self.get_custom_css()
        )

    def generate_cards(self) -> list[genanki.Note]:
        model = self.create_model()
        notes = []

        for char, morse in self.MORSE_CODE.items():
            audio_tag = f'[sound:morse_{char}.mp3]'
            note = genanki.Note(
                model=model,
                fields=[char, morse, audio_tag],
                guid=self._generate_note_id(char),
                tags=self.metadata.tags + ['morse-to-visual']
            )
            notes.append(note)

        return notes


class AudioToVisualDeck(BaseMorseDeck):
    def create_model(self) -> genanki.Model:
        return genanki.Model(
            self._model_id,
            'Audio to Visual Model',
            fields=[
                {'name': 'Character'},
                {'name': 'MorseCode'},
                {'name': 'Audio'}
            ],
            templates=[{
                'name': 'Audio to Character',
                'qfmt': '''
                    <div class="content">
                        <div class="audio-controls">{{Audio}}</div>
                    </div>
                ''',
                'afmt': '''
                    {{FrontSide}}
                    <hr>
                    <div class="content">
                        <div class="character">{{Character}}</div>
                        <div class="morse">{{MorseCode}}</div>
                    </div>
                '''
            }],
            css=self.get_custom_css()
        )

    def generate_cards(self) -> list[genanki.Note]:
        model = self.create_model()
        notes = []

        for char, morse in self.MORSE_CODE.items():
            audio_tag = f'[sound:morse_{char}.mp3]'
            note = genanki.Note(
                model=model,
                fields=[char, morse, audio_tag],
                guid=self._generate_note_id(char),
                tags=self.metadata.tags + ['audio-to-visual']
            )
            notes.append(note)

        return notes


if __name__ == "__main__":
    # Create Visual to Morse deck
    visual_to_morse = VisualToMorseDeck(
        DeckMetadata(
            title="Morse Code: Character to Audio/Visual Morse",
            tags=["morse-code", "visual-to-morse"],
            description="Practice converting characters to Morse code",
            version="1.0",
        )
    )
    visual_to_morse.save_deck("morse_visual_to_morse.apkg")

    # Create Morse to Visual deck
    morse_to_visual = MorseToVisualDeck(
        DeckMetadata(
            title="Morse Code: Visual Morse to Character/Audio Morse",
            tags=["morse-code", "morse-to-visual"],
            description="Practice converting written Morse code to characters",
            version="1.0",
        )
    )
    morse_to_visual.save_deck("morse_morse_to_visual.apkg")

    # Create Audio to Visual deck
    audio_to_visual = AudioToVisualDeck(
        DeckMetadata(
            title="Morse Code: Audio Morse to Character/Visual Morse",
            tags=["morse-code", "audio-to-visual"],
            description="Practice identifying characters from Morse code audio",
            version="1.0",
        )
    )
    audio_to_visual.save_deck("morse_audio_to_visual.apkg")

    # Clean up media files (only after all decks are created)
    visual_to_morse.cleanup_media()