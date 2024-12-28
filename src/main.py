import librosa

from record import (record_audio, extract_pitch_and_timing, pitch_to_midi, save_to_midi, extract_rhythm_and_pitch,
                    calculate_durations, extract_dynamics, save_to_midi_with_rhythm,
                    extract_polyphonic_notes)

# Record a hummed melody, extract pitches and convert them to midi file
record_audio("hum.wav")
pitches, onset_frames = extract_pitch_and_timing("hum.wav")
print("Pitches:", pitches)
print("Onset frames:", onset_frames)
midi_notes = pitch_to_midi(pitches)
print("MIDI Notes:", midi_notes)
save_to_midi(midi_notes, "output.mid")

# Add rhythm detection and dynamics to create a more expressive midi file
pitches, onset_times = extract_rhythm_and_pitch("hum.wav")
print("Pitches:", pitches)
print("Onset times:", onset_times)
durations = calculate_durations(onset_times)
print("Durations:", durations)
y, sr = librosa.load("hum.wav")
volumes = extract_dynamics(y, sr, onset_frames)
print("Volumes:", volumes)
save_to_midi_with_rhythm(midi_notes, durations, volumes, "output_with_rhythm.mid")

# Add polyphony support if needed
# polyphonic_notes = extract_polyphonic_notes("hum_polyphonic.wav")
# print("Polyphonic Notes:", polyphonic_notes)
