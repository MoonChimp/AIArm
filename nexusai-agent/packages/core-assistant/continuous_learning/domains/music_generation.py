import tensorflow as tf
import numpy as np
import music21
import os

class MusicGenerator:
    def __init__(self, model_path=None):
        self.model = self.build_model() if not model_path else self.load_model(model_path)
        self.initialize_tokenizer()
        
    def build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.LSTM(256, return_sequences=True, input_shape=(None, 256)),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.LSTM(512, return_sequences=True),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(256, activation='softmax')
        ])
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        return model
        
    def initialize_tokenizer(self):
        # Initialize music tokenizer for MIDI processing
        self.note_to_int = {}
        self.int_to_note = {}
        self.build_vocabulary()
        
    def build_vocabulary(self):
        notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        octaves = range(0, 8)
        durations = ['whole', 'half', 'quarter', 'eighth', 'sixteenth']
        
        vocab = []
        for note in notes:
            for octave in octaves:
                for duration in durations:
                    token = f"{note}{octave}_{duration}"
                    vocab.append(token)
                    
        for i, token in enumerate(vocab):
            self.note_to_int[token] = i
            self.int_to_note[i] = token
            
    def generate_music(self, seed_sequence, length=100):
        current_sequence = seed_sequence
        generated_notes = []
        
        for _ in range(length):
            prediction = self.model.predict(current_sequence)
            next_note = np.argmax(prediction[0])
            generated_notes.append(self.int_to_note[next_note])
            
            current_sequence = np.roll(current_sequence, -1)
            current_sequence[-1] = next_note
            
        return self.convert_to_midi(generated_notes)
        
    def convert_to_midi(self, notes):
        midi_stream = music21.stream.Stream()
        
        for note_str in notes:
            note, duration = note_str.split('_')
            n = music21.note.Note(note)
            n.duration.type = duration
            midi_stream.append(n)
            
        return midi_stream
        
    def save_midi(self, midi_stream, filename):
        midi_stream.write('midi', fp=filename)

if __name__ == "__main__":
    generator = MusicGenerator()
    print("Music Generation System initialized successfully")