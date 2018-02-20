#!/usr/bin/env python3

import os
def main():
    while True:
        prompt = os.getcwd() + " > "
        command = input(prompt)
        print(command)

if __name__ == "__main__":
    main()
