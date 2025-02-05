#!/usr/bin/env python3
#
# MC4 Cheat Decrypter v0.1 by stoykow
# Based on bucanero's original C implementation

import sys
import os
import base64
import argparse
from Crypto.Cipher import AES

# 32-byte ASCII key, 16-byte ASCII IV (credits to bucanero for reversing this)
MC4_AES256CBC_KEY = b"304c6528f659c766110239a51cl5dd9c"
MC4_AES256CBC_IV  = b"u@}kzW2u[u(8DWar"

def read_buffer(filename):
    """Read entire file into a bytes object."""
    with open(filename, "rb") as f:
        data = f.read()
    return data, len(data)

def write_buffer(filename, data):
    """Write bytes to a file."""
    with open(filename, "wb") as f:
        f.write(data)

def pkcs7_unpad(data):
    """
    Remove PKCS#7 padding from decrypted data.
    If the last byte is n, and the last n bytes are all n, remove them.
    """
    if not data:
        return data
    last_byte = data[-1]
    # last_byte is an integer [0..255]
    pad_len = last_byte
    # Basic checks
    if pad_len < 1 or pad_len > 16:
        return data
    # Check if the last 'pad_len' bytes are the same value 'pad_len'
    if data.endswith(bytes([last_byte]) * pad_len):
        return data[:-pad_len]
    else:
        return data

def decrypt_data(data):
    """
    1) Base64-decode data
    2) AES-256-CBC decrypt (no special block-by-block unpadding)
    3) Remove PKCS#7 padding
    4) Return final decrypted bytes
    """
    print(f"[*] Base64 Encoded Size: {len(data)} bytes")

    try:
        bin_data = base64.b64decode(data)
    except Exception:
        print("Base64 Error!")
        return data  # Return original to avoid crash

    print(f"[*] Total Decrypted Size: {len(bin_data)} bytes")

    # AES in CBC mode
    cipher = AES.new(MC4_AES256CBC_KEY, AES.MODE_CBC, IV=MC4_AES256CBC_IV)
    decrypted = cipher.decrypt(bin_data)

    # Remove PKCS#7 padding
    unpadded = pkcs7_unpad(decrypted)

    print("[*] Decrypted File Successfully!\n")
    return unpadded

def pkcs7_pad(data, block_size=16):
    """
    Add PKCS#7 padding to 'data' so its length becomes a multiple of 'block_size'.
    If 'len(data)' is already a multiple of 'block_size', a full block of padding is added.
    """
    pad_len = block_size - (len(data) % block_size)
    if pad_len == 0:
        pad_len = block_size
    return data + bytes([pad_len] * pad_len)

def encrypt_data(data):
    """
    1) PKCS#7-pad the data
    2) AES-256-CBC encrypt the padded data
    3) Base64-encode the result
    4) Return the Base64 bytes
    """
    print(f"[*] Total XML Size: {len(data)} bytes")

    # 1) PKCS#7 padding
    padded_data = pkcs7_pad(data, 16)
    print(f"[*] Size after PKCS#7 padding: {len(padded_data)} bytes")

    # 2) AES-256-CBC encrypt
    cipher = AES.new(MC4_AES256CBC_KEY, AES.MODE_CBC, IV=MC4_AES256CBC_IV)
    encrypted = cipher.encrypt(padded_data)

    # 3) Base64-encode
    try:
        b64_data = base64.b64encode(encrypted)
    except Exception:
        print("Base64 Error!")
        return data

    print(f"[*] Total Encrypted Size (Base64): {len(b64_data)} bytes")
    print("[*] Encrypted File Successfully!\n")

    # 4) Return final result
    return b64_data

def main():
    parser = argparse.ArgumentParser(
        description=(
            "MC4 Cheat Decrypter v0.1 by stoykow\n"
            "Based on bucanero's original C implementation\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    # Mutually exclusive group for -d / --decrypt or -e / --encrypt
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--decrypt", action="store_true", help="Decrypt file => output .shn")
    group.add_argument("-e", "--encrypt", action="store_true", help="Encrypt file => output .mc4")

    parser.add_argument("cheat_file", type=str, help="cheat file to process")

    args = parser.parse_args()

    print("\nMC4 Cheat Decrypter v0.1 by stoykow\nBased on bucanero's original C implementation\n")

    # Input file
    cheat_file = args.cheat_file
    if not os.path.isfile(cheat_file):
        print(f"[*] Could Not Access The File ({cheat_file})")
        sys.exit(-1)

    # Read the file
    data, length = read_buffer(cheat_file)

    # Figure out output name:
    # For decrypt => produce "xxx.shn"
    # For encrypt => produce "xxx.mc4"
    base, ext = os.path.splitext(cheat_file)
    if args.decrypt:
        output_name = base + ".shn"
        new_data = decrypt_data(data)
    else:
        output_name = base + ".mc4"
        new_data = encrypt_data(data)

    # Write the new file
    write_buffer(output_name, new_data)
    print(f"[*] Wrote output file: {output_name}")

if __name__ == "__main__":
    main()
