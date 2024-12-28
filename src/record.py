import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import librosa
from midiutil import MIDIFile


def record_audio(filename, duration=5, samplerate=44100):
    print("Recording... Hum your melody!")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()  # Wait for the recording to finish
    print("Recording complete!")
    wav.write(filename, samplerate, np.int16(audio * 32767))


def extract_pitch_and_timing(audio_file):
    y, sr = librosa.load(audio_file)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)

    # Get dominant pitch for each onset frame
    pitch_sequence = []
    for frame in onset_frames:
        pitch = pitches[:, frame].max()
        if pitch > 0:  # Filter out frames with no detected pitch
            pitch_sequence.append(pitch)
    return pitch_sequence, onset_frames


def pitch_to_midi(pitch_sequence):
    midi_notes = []
    for pitch in pitch_sequence:
        midi_note = int(69 + 12 * np.log2(pitch / 440.0))  # A440 is MIDI 69
        midi_notes.append(midi_note)
    return midi_notes


def save_to_midi(midi_notes, filename):
    midi = MIDIFile(1)  # Create a single-track MIDI file
    track = 0
    time = 0  # Start time
    midi.addTempo(track, time, 120)  # Set tempo (BPM)

    for i, note in enumerate(midi_notes):
        duration = 1  # Fixed duration for simplicity
        midi.addNote(track, channel=0, pitch=note, time=i, duration=duration, volume=100)

    with open(filename, "wb") as output_file:
        midi.writeFile(output_file)
    print(f"MIDI file saved as {filename}")

def extract_rhythm_and_pitch(audio_file):
    y, sr = librosa.load(audio_file)

    # Onset times
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    # Pitch extraction
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_sequence = []
    for frame in onset_frames:
        pitch = pitches[:, frame].max()
        if pitch > 0:  # Ignore frames with no pitch
            pitch_sequence.append(pitch)

    return pitch_sequence, onset_times


def calculate_durations(onset_times):
    durations = []
    for i in range(len(onset_times) - 1):
        durations.append(onset_times[i + 1] - onset_times[i])
    durations.append(1.0)  # Set default duration for the last note
    return durations


def extract_dynamics(y, sr, onset_frames):
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    volumes = []
    for frame in onset_frames:
        volume = magnitudes[:, frame].max()
        volumes.append(int(volume * 127))  # Scale volume to MIDI range (0-127)
    return volumes


def save_to_midi_with_rhythm(midi_notes, durations, volumes, filename):
    midi = MIDIFile(1)  # Single-track MIDI
    track = 0
    time = 0
    midi.addTempo(track, time, 120)

    for i, note in enumerate(midi_notes):
        duration = durations[i]
        volume = volumes[i]
        midi.addNote(track, channel=0, pitch=note, time=time, duration=duration, volume=volume)
        time += duration  # Update time for the next note

    with open(filename, "wb") as output_file:
        midi.writeFile(output_file)
    print(f"MIDI file with rhythm and dynamics saved as {filename}")


def extract_polyphonic_notes(audio_file):
    y, sr = librosa.load(audio_file)

    # Extract pitch and magnitude with piptrack
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

    # Initialize list for simultaneous notes
    notes = []

    # Loop through each time frame
    for t in range(pitches.shape[1]):
        # Extract all peaks (pitches) at time frame 't' (considering non-zero magnitudes)
        peaks = []
        for f in range(pitches.shape[0]):
            if magnitudes[f, t] > 0:
                peak_pitch = pitches[f, t]
                if peak_pitch > 0:
                    peaks.append(peak_pitch)
        if peaks:
            notes.append(peaks)

    return notes