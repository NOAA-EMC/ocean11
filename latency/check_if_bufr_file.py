#!/usr/bin/env python3

def is_bufr_file(filepath):
    """Check if a file is a BUFR file by looking for 'BUFR' magic bytes."""
    try:
        with open(filepath, 'rb') as f:
            magic = f.read(4)
            return magic == b'BUFR'
    except Exception:
        return False


if __name__ == '__main__':
    import sys
    
    # Check if filepath argument is provided
    if len(sys.argv) != 2:
        print("Usage: python bufr_checker.py <filepath>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    if is_bufr_file(filepath):
        print(f"{filepath} is a BUFR file")
    else:
        print(f"{filepath} is not a BUFR file")
