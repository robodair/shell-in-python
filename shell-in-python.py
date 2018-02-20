#!/usr/bin/env python3

import os
import sys
import shlex


class Builtin(object):
    this_cmd = None
    @classmethod
    def is_command(cls, cmd):
        if cmd[0] == cls.this_cmd:
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
        #TODO: extra validation on the arguments, including checking length
        try:
            var, val = cmd[1].split("=")
            os.environ[var] = val
        except ValueError:
            print("'" + cmd[1] + "'", "is an invalid assignment")


class InteractiveREPL(object):

    builtin_commands = [BuiltinExit, BuiltinEnv, BuiltinExport]

    def run(self):
        while True:
            prompt = os.getcwd() + " > "
            command = input(prompt)
            command = shlex.split(command)

            if command:
                is_builtin = False
                for builtin in self.builtin_commands:
                    if builtin.is_command(command):
                        is_builtin = True
                        builtin().execute(command)
                        break

                if not is_builtin:
                    print("Would run non-builtin command:", command)


            else:
                print("Enter something!")
                continue


if __name__ == "__main__":
    repl = InteractiveREPL()
    repl.run()
