#!/usr/bin/env python3

import os
import sys

def main():
    while True:
        prompt = os.getcwd() + " > "
        command = input(prompt)
        print(command)

        if command == "exit":
            sys.exit()

if __name__ == "__main__":
    main()
