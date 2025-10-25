"""
Random Melody Generator - Inspired by Beethoven, Mozart, and Eminem
====================================================================
This script generates random piano melodies with characteristics inspired by
classical composers (Beethoven, Mozart) and Eminem's rhythmic patterns.

Requirements:
- music21 library: pip install music21
- A MIDI player or DAW to play the generated files
"""

import random
import os
from music21 import stream, note, chord, tempo, instrument, midi, duration, meter
from datetime import datetime

class MelodyGenerator:
    def __init__(self):
        # Define style parameters for each artist
        self.styles = {
            "beethoven": {
                "note_range": list(range(48, 84)),  # C3 to C6
                "durations": [0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 4.0],  # Favor quarter and half notes
                "dynamics": ["p", "mp", "mf", "f", "ff"],  # Dramatic dynamics
                "tempo_range": (60, 100),  # Moderately slow to moderately fast
                "phrase_lengths": [4, 8, 8, 8, 12],  # Common classical phrase structures
                "chord_probability": 0.2,  # Higher chance of chords
                "rest_probability": 0.08,
                "scale": [0, 2, 3, 5, 7, 8, 10, 12],  # Minor scale (dramatic)
                "interval_weights": [8, 5, 3, 2, 1, 1],  # Favor stepwise motion but with some leaps
                "repeated_notes_probability": 0.1
            },
            "mozart": {
                "note_range": list(range(55, 84)),  # G3 to C6, higher register
                "durations": [0.25, 0.25, 0.5, 0.5, 0.5, 0.5, 1.0, 1.0, 1.5, 2.0],  # More varied, more 16th notes
                "dynamics": ["p", "mp", "mf"],  # More delicate dynamics
                "tempo_range": (90, 130),  # Faster, lighter feel
                "phrase_lengths": [4, 4, 8, 8],  # Regular phrases
                "chord_probability": 0.1,  # Fewer chords
                "rest_probability": 0.05,
                "scale": [0, 2, 4, 5, 7, 9, 11, 12],  # Major scale (lighter)
                "interval_weights": [10, 6, 3, 1, 1, 0],  # More stepwise motion
                "repeated_notes_probability": 0.15
            },
            "eminem": {
                "note_range": list(range(48, 72)),  # Lower range
                "durations": [0.25, 0.25, 0.25, 0.25, 0.5, 0.5, 0.75, 1.0],  # Very rhythmic, shorter notes
                "dynamics": ["mf", "f", "ff"],  # Stronger dynamics
                "tempo_range": (85, 110),  # Hip-hop tempo range
                "phrase_lengths": [4, 4, 4, 8],  # Regular, shorter phrases
                "chord_probability": 0.05,  # Focus on single notes
                "rest_probability": 0.15,  # More rests for rhythmic feel
                "scale": [0, 2, 3, 5, 7, 10, 12],  # Minor pentatonic with blue note
                "interval_weights": [12, 4, 2, 1, 0, 0],  # Mostly small intervals with occasional jumps
                "repeated_notes_probability": 0.3  # Repeated notes for rhythmic emphasis
            }
        }
        
    def generate_melody(self, style_name, num_measures=16):
        """Generate a melody in the given style"""
        if style_name.lower() not in self.styles:
            raise ValueError(f"Style '{style_name}' not found. Available styles: {list(self.styles.keys())}")
        
        # Get style parameters
        style = self.styles[style_name.lower()]
        
        # Create stream
        melody = stream.Stream()
        
        # Set instrument to piano
        piano = instrument.Piano()
        melody.append(piano)
        
        # Set random tempo within range
        bpm = random.randint(style["tempo_range"][0], style["tempo_range"][1])
        melody.append(tempo.MetronomeMark(number=bpm))
        
        # Set time signature to 4/4
        melody.append(meter.TimeSignature('4/4'))
        
        # Generate random seed pitch
        current_pitch = random.choice(style["note_range"])
        
        # Track the current beat position within the measure
        current_beat = 0.0
        measure_length = 4.0  # 4/4 time
        
        # Generate a phrase structure based on style
        phrases = []
        total_measures = 0
        while total_measures < num_measures:
            phrase_length = random.choice(style["phrase_lengths"])
            if total_measures + phrase_length <= num_measures:
                phrases.append(phrase_length)
                total_measures += phrase_length
            else:
                phrases.append(num_measures - total_measures)
                total_measures = num_measures
        
        # Generate the melody phrase by phrase
        for phrase_measures in phrases:
            phrase_notes = []
            phrase_beat = 0
            
            while phrase_beat < phrase_measures * measure_length:
                # Decide whether to insert a rest
                if random.random() < style["rest_probability"]:
                    # Add a rest
                    rest_duration = random.choice(style["durations"])
                    if phrase_beat + rest_duration > phrase_measures * measure_length:
                        rest_duration = phrase_measures * measure_length - phrase_beat
                    
                    r = note.Rest()
                    r.duration = duration.Duration(rest_duration)
                    phrase_notes.append(r)
                    phrase_beat += rest_duration
                    continue
                
                # Decide whether to create a chord
                if random.random() < style["chord_probability"]:
                    # Generate a chord
                    root = random.choice(style["note_range"])
                    
                    # Simple triad chord
                    chord_type = random.choice(["major", "minor"])
                    if chord_type == "major":
                        chord_notes = [root, root + 4, root + 7]
                    else:
                        chord_notes = [root, root + 3, root + 7]
                    
                    c = chord.Chord(chord_notes)
                    note_duration = random.choice(style["durations"])
                    
                    # Ensure we don't exceed the phrase length
                    if phrase_beat + note_duration > phrase_measures * measure_length:
                        note_duration = phrase_measures * measure_length - phrase_beat
                    
                    c.duration = duration.Duration(note_duration)
                    c.volume.velocity = random.randint(70, 110)
                    phrase_notes.append(c)
                    phrase_beat += note_duration
                    current_pitch = root
                else:
                    # Generate a single note
                    
                    # Decide whether to repeat the current pitch
                    if random.random() < style["repeated_notes_probability"]:
                        # Keep the same pitch
                        pass
                    else:
                        # Choose a new pitch based on interval weights
                        max_interval = len(style["interval_weights"]) - 1
                        
                        # Determine direction (up or down)
                        direction = random.choice([-1, 1])
                        
                        # Choose interval size based on weights
                        interval = random.choices(
                            range(max_interval + 1),
                            weights=style["interval_weights"],
                            k=1
                        )[0]
                        
                        # Calculate target scale degree
                        scale_note = direction * interval
                        
                        # Create array of possible pitches
                        possible_pitches = []
                        for pitch in style["note_range"]:
                            # Check if it's in the scale
                            if (pitch % 12) in [n % 12 for n in style["scale"]]:
                                possible_pitches.append(pitch)
                        
                        # Find closest matching pitch
                        closest_pitch = min(possible_pitches, key=lambda p: abs(p - (current_pitch + scale_note)))
                        
                        # Update current pitch
                        current_pitch = closest_pitch
                    
                    # Create the note
                    n = note.Note(current_pitch)
                    note_duration = random.choice(style["durations"])
                    
                    # Ensure we don't exceed the phrase length
                    if phrase_beat + note_duration > phrase_measures * measure_length:
                        note_duration = phrase_measures * measure_length - phrase_beat
                    
                    n.duration = duration.Duration(note_duration)
                    
                    # Set random dynamic
                    n.dynamic = random.choice(style["dynamics"])
                    phrase_notes.append(n)
                    phrase_beat += note_duration
            
            # Add phrase to melody
            for n in phrase_notes:
                melody.append(n)
        
        return melody
    
    def save_midi(self, melody, style_name, output_dir="melodies"):
        """Save the melody as a MIDI file"""
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{style_name}_{timestamp}.mid"
        filepath = os.path.join(output_dir, filename)
        
        # Write MIDI file
        mf = midi.translate.streamToMidiFile(melody)
        mf.open(filepath, 'wb')
        mf.write()
        mf.close()
        
        return filepath

def generate_samples():
    """Generate sample melodies for each style"""
    generator = MelodyGenerator()
    
    output_dir = "melodies"
    
    for style in ["beethoven", "mozart", "eminem"]:
        print(f"Generating {style} melody...")
        melody = generator.generate_melody(style, num_measures=16)
        filepath = generator.save_midi(melody, style, output_dir)
        print(f"Saved to {filepath}")

if __name__ == "__main__":
    print("Random Melody Generator - Inspired by Beethoven, Mozart, and Eminem")
    print("================================================================")
    generate_samples()
    print("\nDone! Check the 'melodies' folder for the generated MIDI files.")
    print("You can play these files with any MIDI player or import them into a DAW.")
