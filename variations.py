import mido
from mido import MidiFile, MidiTrack, Message


def transpose_midi(input_file, output_file, transpose_amount):
    mid = MidiFile(input_file)
    new_mid = MidiFile()

    for i, track in enumerate(mid.tracks):
        new_track = MidiTrack()
        new_mid.tracks.append(new_track)

        for msg in track:
            # Only transpose 'note_on' and 'note_off' messages
            if msg.type == 'note_on' or msg.type == 'note_off':
                msg.note += transpose_amount  # Transpose the note by the specified amount
            new_track.append(msg)

    new_mid.save(output_file)
    print(f"Transposed MIDI saved as {output_file}")


# Example: Transpose by 5 semitones
transpose_midi("output.mid", "transposed_output.mid", 5)
