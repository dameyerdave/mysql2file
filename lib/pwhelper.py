#!/usr/bin/env python

import sys, base64

class PWHelper:
    @staticmethod
    def encode(plaintext):
        ciphertext = "".join(chr(ord(x) ^ ord(y)) for x, y in zip(plaintext, '4RNxuKJX8JFrHwhAz7ZKrtYw'))
        return base64.b64encode(ciphertext).encode()

    @staticmethod
    def decode(ciphertext):
        ciphertext = base64.b64decode(ciphertext).decode()
        plaintext = "".join(chr(ord(x) ^ ord(y)) for x, y in zip(ciphertext, '4RNxuKJX8JFrHwhAz7ZKrtYw'))
        return plaintext

if __name__ == "__main__":
    print(PWHelper.encode(sys.argv[1]))
