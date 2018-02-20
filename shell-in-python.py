#!/usr/bin/env python3

import os
import sys

class BuiltinExit(object):

    this_cmd = "exit"

    @classmethod
    def is_command(cls, cmd):
        if cmd == cls.this_cmd:
            return True
        return False

    def execute(self, cmd):
        # TODO: Check if there's the right number of args or not
        sys.exit(0)


class InteractiveREPL(object):

    builtin_commands = [BuiltinExit]

    def run(self):
        while True:
            prompt = os.getcwd() + " > "
            command = input(prompt)

            if command:
                for builtin in self.builtin_commands:
                    if builtin.is_command(command):
                        builtin().execute(command)
            else:
                # nothing, empty line
                continue

            print(command)


if __name__ == "__main__":
    repl = InteractiveREPL()
    repl.run()
