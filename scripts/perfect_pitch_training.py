from io import BytesIO

from pydub import AudioSegment

from base import AnkiDeck, DeckMetadata
import genanki
import numpy as np
from scipy.io import wavfile
import os
import random


class PerfectPitchDeck(AnkiDeck):
    SAMPLE_RATE = 44100  # Hz
    DURATION = 1.0  # seconds
    AMPLITUDE = 0.3
    BASE_NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    OCTAVES = range(3, 6)  # C3 to B5

    def __init__(self, metadata: DeckMetadata):
        super().__init__(metadata)
        self.note_frequencies = self._generate_frequencies()

    def _generate_frequencies(self) -> dict[str, float]:
        """Generate frequencies for all notes."""
        frequencies = {}
        A4_FREQ = 440.0
        A4_OCTAVE = 4
        A4_NOTE = 9  # Index of A in BASE_NOTES

        for octave in self.OCTAVES:
            for note in self.BASE_NOTES:
                note_name = f"{note}{octave}"
                note_idx = self.BASE_NOTES.index(note)
                semitone_distance = (octave - A4_OCTAVE) * 12 + (note_idx - A4_NOTE)
                frequencies[note_name] = A4_FREQ * (2 ** (semitone_distance / 12.0))
        return frequencies

    def _generate_piano_like_tone(self, frequency: float) -> np.ndarray:
        """Generate a more pleasant piano-like tone with harmonics."""
        t = np.linspace(0, self.DURATION, int(self.SAMPLE_RATE * self.DURATION), False)

        tone = np.zeros_like(t)
        harmonics = [1, 2, 3, 4]
        harmonic_weights = [1.0, 0.5, 0.25, 0.125]

        for harmonic, weight in zip(harmonics, harmonic_weights):
            tone += weight * np.sin(2 * np.pi * frequency * harmonic * t)

        tone = tone / np.max(np.abs(tone))

        total_samples = len(tone)
        attack_samples = int(0.02 * self.SAMPLE_RATE)
        decay_samples = int(0.1 * self.SAMPLE_RATE)
        sustain_level = 0.7
        release_samples = int(0.3 * self.SAMPLE_RATE)

        envelope = np.ones(total_samples) * sustain_level
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        envelope[attack_samples:attack_samples + decay_samples] = np.linspace(1, sustain_level, decay_samples)
        envelope[-release_samples:] = np.linspace(sustain_level, 0, release_samples)

        return (tone * envelope * self.AMPLITUDE * 32767).astype(np.int16)

    def _save_audio_as_mp3(self, audio_data: np.ndarray, filename: str):
        """Convert numpy array to MP3 file using pydub."""
        # First save as WAV in memory
        wav_io = BytesIO()
        wavfile.write(wav_io, self.SAMPLE_RATE, audio_data)
        wav_io.seek(0)

        # Convert to MP3
        audio_segment = AudioSegment.from_wav(wav_io)
        audio_segment.export(filename, format="mp3", bitrate="192k")

    def create_model(self) -> genanki.Model:
        return genanki.Model(
            self._model_id,
            'Perfect Pitch Training',
            fields=[
                {'name': 'Audio'},
                {'name': 'Note'},
                {'name': 'Octave'},
                {'name': 'Frequency'},
            ],
            templates=[{
                'name': 'Perfect Pitch Card',
                'qfmt': '''
                    {{Audio}}
                    <div class="question">What note is this?</div>
                ''',
                'afmt': '''
                    {{Audio}}
                    <div class="answer">
                        <div class="note">{{Note}}</div>
                        <div class="details">
                            Octave: {{Octave}}<br>
                            Frequency: {{Frequency}} Hz
                        </div>
                    </div>
                '''
            }],
            css='''
                .card {
                    font-family: Arial, sans-serif;
                    font-size: 28px;
                    text-align: center;
                    color: black;
                    background-color: white;
                    padding: 20px;
                }
                .question {
                    margin-top: 20px;
                }
                .answer {
                    margin-top: 20px;
                }
                .note {
                    color: #2196F3;
                    font-weight: bold;
                    font-size: 36px;
                }
                .details {
                    color: #666;
                    font-size: 18px;
                    margin-top: 10px;
                }
            '''
        )

    def generate_cards(self) -> list[genanki.Note]:
        model = self.create_model()
        notes = []
        note_data = []

        for note_name, frequency in self.note_frequencies.items():
            note_data.append((note_name, frequency))

        random.shuffle(note_data)

        for note_name, frequency in note_data:
            audio_data = self._generate_piano_like_tone(frequency)
            audio_filename = f'note_{note_name.replace("#", "sharp")}.mp3'
            self._save_audio_as_mp3(audio_data, audio_filename)
            self.media_files.append(audio_filename)

            octave = note_name[-1]
            note_without_octave = note_name[:-1]
            note = genanki.Note(
                model=model,
                fields=[
                    f'[sound:{audio_filename}]',
                    note_without_octave,
                    octave,
                    f'{frequency:.2f}'
                ]
            )
            notes.append(note)

        return notes

    def cleanup(self):
        """Clean up generated audio files."""
        for file in self.media_files:
            os.remove(file)


if __name__ == "__main__":
    deck = PerfectPitchDeck(
        DeckMetadata(
            title="Perfect Pitch Training",
            tags=["music", "ear-training", "perfect-pitch"],
            description="A deck designed to help develop perfect pitch through ear training exercises.",
            version="1.0"
        )
    )
    deck.save_deck("perfect_pitch_training.apkg")
    deck.cleanup()