import struct
import csv

def read_short(f):
    return struct.unpack('<h', f.read(2))[0]

def read_byte(f):
    return struct.unpack('<B', f.read(1))[0]

def read_int(f):
    return struct.unpack('<i', f.read(4))[0]

def read_string(f):
    length = struct.unpack('<i', f.read(4))[0]
    return f.read(length).decode('utf-8')

def skip_header(f):
    if read_short(f) != 0:
        raise ValueError("This does not appear to be a new-format NBS file.")
    
    read_byte(f)  # NBS version
    read_byte(f)  # Vanilla instrument count
    read_short(f)  # Song length
    read_short(f)  # Layer count

    read_string(f)  # Song name
    read_string(f)  # Song author
    read_string(f)  # Original author
    read_string(f)  # Description

    read_short(f)   # Tempo
    read_byte(f)    # Auto-saving
    read_byte(f)    # Auto-saving duration
    read_byte(f)    # Time signature
    read_int(f)     # Minutes spent
    read_int(f)     # Left-clicks
    read_int(f)     # Right-clicks
    read_int(f)     # Note blocks added
    read_int(f)     # Note blocks removed
    read_string(f)  # MIDI/Schematic file name
    read_byte(f)    # Loop on/off
    read_byte(f)    # Max loop count
    read_short(f)   # Loop start tick

def main():
    filename = input("Enter the .nbs filename: ")
    output_file = input("Enter output filename (e.g. output.csv): ")

    try:
        with open(filename, "rb") as f, open(output_file, "w", newline='') as out:
            skip_header(f)  # Skip all metadata before the note data
            tick = -1

            writer = csv.writer(out)
            writer.writerow(["tick", "instrument", "key"])

            while True:
                jump_ticks = read_short(f)
                if jump_ticks == 0:
                    break
                tick += jump_ticks

                while True:
                    jump_layers = read_short(f)
                    if jump_layers == 0:
                        break

                    instrument = struct.unpack('<B', f.read(1))[0]
                    key = struct.unpack('<B', f.read(1))[0] - 33  # Subtract 33 as per NBS key encoding

                    f.read(1 + 1 + 2)  # Skip velocity, panning, pitch

                    writer.writerow([tick // 2, instrument, key])

        print(f"CSV data saved to {output_file}")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
