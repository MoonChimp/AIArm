"""
Interactive Melody Generator - Inspired by Beethoven, Mozart, and Eminem
=======================================================================
This script provides an interactive command-line interface to generate and play
random melodies inspired by different musical styles.

Requirements:
- music21 library: pip install music21
- pygame: pip install pygame (for playback)
"""

import os
import sys
import time
import random
import pygame
from music21 import stream, note, chord, tempo, instrument, midi, duration, meter
from datetime import datetime

class MelodyPlayer:
    """Class to play MIDI files using pygame"""
    
    def __init__(self):
        pygame.mixer.init()
        pygame.init()
    
    def play_midi(self, midi_file):
        """Play a MIDI file"""
        try:
            pygame.mixer.music.load(midi_file)
            pygame.mixer.music.play()
            
            # Print info while playing
            print(f"▶️ Now playing: {os.path.basename(midi_file)}")
            print("   Press Ctrl+C to stop and return to menu...")
            
            # Wait for music to finish playing
            while pygame.mixer.music.get_busy():
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            # Stop playback if user presses Ctrl+C
            pygame.mixer.music.stop()
            print("\nPlayback stopped.")
        except Exception as e:
            print(f"Error playing MIDI file: {e}")
    
    def cleanup(self):
        """Clean up pygame resources"""
        pygame.mixer.quit()
        pygame.quit()

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
        
        # Track generated melodies
        self.generated_melodies = []
        
    def generate_melody(self, style_name, num_measures=16, custom_params=None):
        """Generate a melody in the given style"""
        if style_name.lower() not in self.styles:
            raise ValueError(f"Style '{style_name}' not found. Available styles: {list(self.styles.keys())}")
        
        # Get style parameters
        style = self.styles[style_name.lower()].copy()
        
        # Apply any custom parameters
        if custom_params:
            for key, value in custom_params.items():
                if key in style:
                    style[key] = value
        
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
        
        # Add to generated melodies list
        self.generated_melodies.append({
            "style": style_name,
            "filename": filename,
            "filepath": filepath,
            "timestamp": timestamp
        })
        
        return filepath
    
    def list_generated_melodies(self):
        """List all generated melodies"""
        if not self.generated_melodies:
            print("No melodies have been generated yet.")
            return []
        
        print("\nGenerated Melodies:")
        print("-------------------")
        for i, melody in enumerate(self.generated_melodies):
            print(f"{i+1}. {melody['style'].capitalize()} - {melody['filename']}")
        
        return self.generated_melodies

class InteractiveMelodyApp:
    """Interactive command-line application for melody generation"""
    
    def __init__(self):
        self.generator = MelodyGenerator()
        self.player = MelodyPlayer()
        self.output_dir = "melodies"
        self.running = True
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "=" * 65)
        print("  INTERACTIVE MELODY GENERATOR - Beethoven, Mozart, and Eminem")
        print("=" * 65)
        print("1. Generate a Beethoven-style melody")
        print("2. Generate a Mozart-style melody")
        print("3. Generate an Eminem-style melody")
        print("4. Generate a custom melody")
        print("5. List and play generated melodies")
        print("6. Exit")
        print("=" * 65)
    
    def get_custom_parameters(self):
        """Get custom parameters from user"""
        custom_params = {}
        
        print("\nCustom Melody Parameters (press Enter to use defaults)")
        
        # Choose base style
        print("\nSelect a base style to customize:")
        print("1. Beethoven")
        print("2. Mozart")
        print("3. Eminem")
        
        style_choice = input("Enter choice (1-3): ").strip()
        
        if style_choice == "1":
            base_style = "beethoven"
        elif style_choice == "2":
            base_style = "mozart"
        elif style_choice == "3":
            base_style = "eminem"
        else:
            print("Invalid choice. Using Beethoven as base style.")
            base_style = "beethoven"
        
        # Get number of measures
        measures = input("Number of measures (4-32): ").strip()
        if measures.isdigit() and 4 <= int(measures) <= 32:
            num_measures = int(measures)
        else:
            num_measures = 16
            print(f"Using default: {num_measures} measures")
        
        # Get tempo range
        tempo_min = input("Minimum tempo (40-200): ").strip()
        tempo_max = input("Maximum tempo (40-200): ").strip()
        
        if tempo_min.isdigit() and tempo_max.isdigit():
            t_min = int(tempo_min)
            t_max = int(tempo_max)
            
            if 40 <= t_min <= 200 and 40 <= t_max <= 200 and t_min <= t_max:
                custom_params["tempo_range"] = (t_min, t_max)
                print(f"Tempo range set to: {t_min}-{t_max} BPM")
            else:
                print("Invalid tempo range. Using default.")
        
        # Get chord probability
        chord_prob = input("Chord probability (0.0-1.0): ").strip()
        try:
            cp = float(chord_prob)
            if 0.0 <= cp <= 1.0:
                custom_params["chord_probability"] = cp
                print(f"Chord probability set to: {cp}")
            else:
                print("Invalid chord probability. Using default.")
        except ValueError:
            pass
        
        # Get rest probability
        rest_prob = input("Rest probability (0.0-1.0): ").strip()
        try:
            rp = float(rest_prob)
            if 0.0 <= rp <= 1.0:
                custom_params["rest_probability"] = rp
                print(f"Rest probability set to: {rp}")
            else:
                print("Invalid rest probability. Using default.")
        except ValueError:
            pass
        
        return base_style, num_measures, custom_params
    
    def run(self):
        """Run the application main loop"""
        print("\nWelcome to the Interactive Melody Generator!")
        print("This application generates random piano melodies inspired by different musical styles.")
        
        while self.running:
            self.display_menu()
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                # Generate Beethoven melody
                print("\nGenerating Beethoven-style melody...")
                melody = self.generator.generate_melody("beethoven", num_measures=16)
                filepath = self.generator.save_midi(melody, "beethoven", self.output_dir)
                print(f"Saved to {filepath}")
                
                # Ask if user wants to play it
                if input("Play this melody? (y/n): ").lower().startswith("y"):
                    self.player.play_midi(filepath)
                
            elif choice == "2":
                # Generate Mozart melody
                print("\nGenerating Mozart-style melody...")
                melody = self.generator.generate_melody("mozart", num_measures=16)
                filepath = self.generator.save_midi(melody, "mozart", self.output_dir)
                print(f"Saved to {filepath}")
                
                # Ask if user wants to play it
                if input("Play this melody? (y/n): ").lower().startswith("y"):
                    self.player.play_midi(filepath)
                
            elif choice == "3":
                # Generate Eminem melody
                print("\nGenerating Eminem-style melody...")
                melody = self.generator.generate_melody("eminem", num_measures=16)
                filepath = self.generator.save_midi(melody, "eminem", self.output_dir)
                print(f"Saved to {filepath}")
                
                # Ask if user wants to play it
                if input("Play this melody? (y/n): ").lower().startswith("y"):
                    self.player.play_midi(filepath)
                
            elif choice == "4":
                # Generate custom melody
                print("\nCustom Melody Generator")
                base_style, num_measures, custom_params = self.get_custom_parameters()
                
                print(f"\nGenerating custom melody based on {base_style} style...")
                melody = self.generator.generate_melody(base_style, num_measures, custom_params)
                filepath = self.generator.save_midi(melody, f"custom_{base_style}", self.output_dir)
                print(f"Saved to {filepath}")
                
                # Ask if user wants to play it
                if input("Play this melody? (y/n): ").lower().startswith("y"):
                    self.player.play_midi(filepath)
                
            elif choice == "5":
                # List and play generated melodies
                melodies = self.generator.list_generated_melodies()
                
                if melodies:
                    melody_choice = input("\nEnter the number of the melody to play (0 to go back): ").strip()
                    
                    if melody_choice.isdigit() and 1 <= int(melody_choice) <= len(melodies):
                        idx = int(melody_choice) - 1
                        selected_melody = melodies[idx]
                        self.player.play_midi(selected_melody["filepath"])
                
            elif choice == "6":
                # Exit
                print("\nThank you for using the Interactive Melody Generator!")
                self.running = False
            
            else:
                print("\nInvalid choice. Please enter a number between 1 and 6.")
    
    def cleanup(self):
        """Clean up resources"""
        self.player.cleanup()

if __name__ == "__main__":
    try:
        # Check if required libraries are installed
        missing_libs = []
        try:
            import music21
        except ImportError:
            missing_libs.append("music21")
        
        try:
            import pygame
        except ImportError:
            missing_libs.append("pygame")
        
        if missing_libs:
            print("Missing required libraries. Please install:")
            for lib in missing_libs:
                print(f"  pip install {lib}")
            sys.exit(1)
        
        # Create and run the application
        app = InteractiveMelodyApp()
        app.run()
        app.cleanup()
        
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
