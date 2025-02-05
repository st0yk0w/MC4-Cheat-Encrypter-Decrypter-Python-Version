# MC4 Cheat Encrypter/Decrypter (Python Version)

This is a **Python** port of the **MC4 Cheat Decrypter** originally written in C by [bucanero](https://github.com/bucanero/save-decrypters/tree/master/mc4-cheat-decrypter).  
It encrypts/decrypts `.mc4` cheat files with AES‐256‐CBC and Base64.

## Features & Improvements

- **PKCS#7 padding** added when encrypting to match the original MC4 format (no trailing garbage bytes).  
- **Separate output files** for encryption/decryption:
  - Decrypting a `.mc4` file produces a `.shn` file (rather than overwriting the original).  
  - Encrypting a `.shn` file produces a `.mc4` file.

## Requirements

1. **Python 3.7+** (earlier versions might work, but tested with 3.7 and up).  
2. **PyCryptodome** for AES:

   ```bash
   pip install pycryptodome
   ```

### Decryption

Decrypting a `.mc4` file produces `<cheat_file>.shn`, eg:

```bash
python mc4_cheat_decrypter.py -d CUSA36582_01.01.mc4
```

- Reads `CUSA36582_01.01.mc4`  
- Decrypts via AES‐256‐CBC (using the built‐in key/IV)  
- Base64‐decodes the input first, unpads PKCS#7 afterward  
- Writes `CUSA36582_01.01.shn`

### Encryption

Encrypting a `.shn` file produces `<cheat_file>.mc4`, eg:

```bash
python mc4_cheat_decrypter.py -e CUSA36582_01.01.shn
```

- Reads `CUSA36582_01.01.shn`  
- Adds PKCS#7 padding to the input  
- Encrypts via AES‐256‐CBC  
- Base64‐encodes the encrypted result  
- Writes `CUSA36582_01.01.mc4`

To see full usage info:

```bash
python mc4_cheat_decrypter.py -h
```
