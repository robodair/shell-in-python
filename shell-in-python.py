#!/usr/bin/env python3

import os
import sys


class Builtin(object):
    this_cmd = None
    @classmethod
    def is_command(cls, cmd):
        if cmd == cls.this_cmd:
            return True
        return False


class BuiltinExit(Builtin):
    this_cmd = "exit"
    def execute(self, cmd):
        # TODO: Check if there's the right number of args or not
        sys.exit(0)


class BuiltinEnv(Builtin):
    this_cmd = "env"
    def execute(self, cmd):
        for var, val in os.environ.items():
            print(var + "=" + val)


class BuiltinExport(Builtin):
    this_cmd = "export"
    def execute(self, cmd):
        print("export command")


class InteractiveREPL(object):

    builtin_commands = [BuiltinExit, BuiltinEnv, BuiltinExport]

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
