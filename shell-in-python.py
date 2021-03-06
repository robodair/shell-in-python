#!/usr/bin/env python3

import os
import sys
import shlex
import subprocess


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


class BuiltinList(Builtin):
    this_cmd = "ls"
    def execute(self, cmd):
        dirs = cmd [1:]
        if not dirs:
            dirs = ["."]
        for d in dirs:
            try:
                contents = os.listdir(d)
                print(d)
                print(contents)
            except FileNotFoundError:
                print(d, "Not Found")
                continue


class BuiltinChdir(Builtin):
    this_cmd = "cd"
    def execute(self, cmd):
        #TODO: only accept one argument
        try:
            d = cmd[1]
        except IndexError:
            d = "."
        os.chdir(d)


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


class ExternalCommand(object):
    def execute(self, command):
        # python subprocess can do the heavy lifting here, we just worry about pipes
        processes = []
        current_process = []

        for segment in command:
            if segment == "|":
                processes.append(current_process)
                current_process = []
            else:
                current_process.append(segment)
        processes.append(current_process) # catch the last process not ending with "|"

        prev_process = None
        stdin = sys.stdin
        for index, process in enumerate(processes):
            stdout = subprocess.PIPE

            last_process = index + 1 == len(processes)

            if last_process:
                stdout = sys.stdout

            prev_process = subprocess.Popen(process, stdout=stdout, stdin=stdin)
            stdin = prev_process.stdout

            if last_process:
                prev_process.wait()


class InteractiveREPL(object):

    builtin_commands = [BuiltinExit, BuiltinEnv, BuiltinExport, BuiltinList, BuiltinChdir]

    def run(self):
        while True:
            prompt = os.getcwd() + " > "
            command = input(prompt)
            command = shlex.split(command)

            if command:
                is_builtin = False
                for builtin in self.builtin_commands:
                    if builtin.is_command(command[0]):
                        is_builtin = True
                        builtin().execute(command)
                        break

                if not is_builtin:
                    ExternalCommand().execute(command)

            else:
                print("Enter something!")
                continue


if __name__ == "__main__":
    repl = InteractiveREPL()
    repl.run()
