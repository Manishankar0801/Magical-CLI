# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 14:33:27 2022

@author: mjanumpa

creating own CLI (shell) in Python

References:
    1. https://docs.python.org/3/library/os.html
    2. https://stackoverflow.com/questions/983354/how-to-make-a-python-script-wait-for-a-pressed-key
    3. https://stackoverflow.com/questions/4906977/how-to-access-environment-variable-values
    4. https://stackoverflow.com/questions/431684/equivalent-of-shell-cd-command-to-change-the-working-directory
    5. https://stackoverflow.com/questions/2084508/clear-terminal-in-python/2084521
    6. https://pythonguides.com/python-exit-command/
"""

import os
import subprocess
import shlex
import sys
from typing import List, Dict, Any
import json
import glob
import datetime
import shutil

class Shell:
    def __init__(self):
        self.commands = {
            "cd": self.change_directory,
            "clr": self.clear_screen,
            "dir": self.list_directory,
            "ls": self.list_current_directory,
            "environ": self.show_environment,
            "echo": self.echo,
            "help": self.show_help,
            "pause": self.pause,
            "quit": self.quit,
            "history": self.show_history,
            "alias": self.manage_alias,
            "find": self.find_files,
            "grep": self.grep,
            "touch": self.touch,
            "cat": self.cat,
            "wc": self.word_count,
            "date": self.show_date,
            "calc": self.calculator,
            "tree": self.directory_tree,
            "todo": self.todo_list,
        }
        self.aliases: Dict[str, str] = {}
        self.history: List[str] = []
        self.todo_items: List[str] = []
        self.load_config()

    def run(self):
        self.print_welcome_message()
        while True:
            try:
                command = input(f"{os.getcwd()} --> ").strip()
                self.history.append(command)
                self.execute(command)
            except KeyboardInterrupt:
                print("\nUse 'quit' to exit the shell.")
            except Exception as e:
                print(f"An error occurred: {e}")

    def execute(self, command: str):
        args = shlex.split(command)
        if not args:
            return

        if args[0] in self.aliases:
            args = shlex.split(self.aliases[args[0]]) + args[1:]

        if args[0] in self.commands:
            self.commands[args[0]](args[1:])
        else:
            self.run_external_command(args)

    def run_external_command(self, args: List[str]):
        try:
            subprocess.run(args, check=True)
        except subprocess.CalledProcessError:
            print(f"'{args[0]}' is not recognized as an internal or external command")

    # ... [previous methods remain unchanged] ...

    def find_files(self, args: List[str]):
        if not args:
            print("Usage: find <pattern>")
            return
        pattern = args[0]
        for file in glob.glob(pattern, recursive=True):
            print(file)

    def grep(self, args: List[str]):
        if len(args) < 2:
            print("Usage: grep <pattern> <file>")
            return
        pattern, file = args[0], args[1]
        try:
            with open(file, 'r') as f:
                for line in f:
                    if pattern in line:
                        print(line.strip())
        except FileNotFoundError:
            print(f"File not found: {file}")

    def touch(self, args: List[str]):
        if not args:
            print("Usage: touch <filename>")
            return
        filename = args[0]
        open(filename, 'a').close()
        print(f"Created or updated: {filename}")

    def cat(self, args: List[str]):
        if not args:
            print("Usage: cat <filename>")
            return
        filename = args[0]
        try:
            with open(filename, 'r') as f:
                print(f.read())
        except FileNotFoundError:
            print(f"File not found: {filename}")

    def word_count(self, args: List[str]):
        if not args:
            print("Usage: wc <filename>")
            return
        filename = args[0]
        try:
            with open(filename, 'r') as f:
                content = f.read()
                lines = content.count('\n')
                words = len(content.split())
                chars = len(content)
                print(f"Lines: {lines}, Words: {words}, Characters: {chars}")
        except FileNotFoundError:
            print(f"File not found: {filename}")

    def show_date(self, args: List[str]):
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def calculator(self, args: List[str]):
        if not args:
            print("Usage: calc <expression>")
            return
        try:
            result = eval(' '.join(args))
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error in calculation: {e}")

    def directory_tree(self, args: List[str]):
        root_dir = args[0] if args else '.'
        for root, dirs, files in os.walk(root_dir):
            level = root.replace(root_dir, '').count(os.sep)
            indent = ' ' * 4 * level
            print(f"{indent}{os.path.basename(root)}/")
            sub_indent = ' ' * 4 * (level + 1)
            for file in files:
                print(f"{sub_indent}{file}")

    def todo_list(self, args: List[str]):
        if not args:
            if not self.todo_items:
                print("No todo items.")
            else:
                for i, item in enumerate(self.todo_items, 1):
                    print(f"{i}. {item}")
        elif args[0] == "add":
            self.todo_items.append(' '.join(args[1:]))
            print("Item added.")
        elif args[0] == "remove":
            try:
                index = int(args[1]) - 1
                removed = self.todo_items.pop(index)
                print(f"Removed: {removed}")
            except (IndexError, ValueError):
                print("Invalid item number.")
        else:
            print("Usage: todo [add <item> | remove <number>]")

    def load_config(self):
        try:
            with open('shell_config.json', 'r') as f:
                config = json.load(f)
                self.aliases = config.get('aliases', {})
                self.todo_items = config.get('todo_items', [])
        except FileNotFoundError:
            pass

    def save_config(self):
        config = {
            'aliases': self.aliases,
            'todo_items': self.todo_items
        }
        with open('shell_config.json', 'w') as f:
            json.dump(config, f)

    def quit(self, args: List[str]):
        self.save_config()
        print("Thank you for using Mani's Magical CLI (Shell). Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    Shell().run()

# import os
# import subprocess as subProcess

# def helpCommand(inp = 0):
#     help_string = ("Below listed are the valid commands that supports in Mani's Magical CLI(Shell):\n"
#                          "\n1. cd <directory> - change the current default directory to <directory>. If the <directory> argument is not present, report the current directory. If the directory does not exist an appropriate error should be reported. This command should also change the PWD environment variable.\n"
#                          "2. clr - clear the screen.\n"
#                          "3. dir <directory> - list the contents of directory <directory>\n"
#                          "4. ls - lists all the contents of current working directory\n"
#                          "5. environ - list all the environment strings\n"
#                          "6. echo <comment> - display <comment> on the display followed by a new line (multiple spaces/tabs may be reduced to a single space)\n"
#                          "7. help - display a list of all commands and their inputs/behaviors that are supported in Mani's Magical CLI(Shell).\n"
#                          "8. pause - pause operation of the shell until 'Enter' is pressed\n"
#                          "9. quit - quit the shell\n"
#                          "\nMani's Magical CLI(Shell) also supports output redireciton\n")
#     help_string_split = help_string.split("\n")
#     if inp == ">":
#         l=[]
#         l.append("\n")
#         for i in range(len(help_string_split)):
#             l.append(help_string_split[i])
#         return l
#     print(help_string)
#     return

# def quit():
#     print()
#     print("Thank's for using Mani's Magical CLI(shell)")
#     print("Bye Bye...!!!")
#     os._exit(0)

# def ls(inp=0):
#     contents = os.listdir(os.getcwd())
#     if inp == ">":
#         l=[]
#         l.append("\n")
#         for i in contents:
#             l.append(i)
#         return l
#     print()
#     print("Contents in the current directory ",os.getcwd(), " are listed below: ")
#     print()
#     for content in contents:
#         print(content)

# def clr():
#     #os.system('cls' if os.name == 'nt' else 'clear')
#     print("\x1b[2J\x1b[H",end="")


# def cd(args):
#     try:
#         if args == ">":
#             args = 0
#             if args ==0:
#                 l=[]
#                 l.append(os.getcwd()+"\n")
#                 return(l)
#         if len(args) == 0:
#             print(os.getcwd())
#         else:
#             return os.chdir(args)
#     except Exception:
#         print(args," No such File or Directory Exists")

# def directory(d=0):

#     if d == ">":
#         l=[]
#         l.append("\n")
#         for i in os.listdir(os.getcwd()):
#             l.append(i)
#         return l
#     if d==0:
#         for i in os.listdir(os.getcwd()):
#             print(i)
#     else:
#         if ">" == d[-1]:
#             l=[]
#             y = d[:-1].strip()
#             for i in os.listdir(y):
#                 l.append(i)
#             return l
#         if os.path.isdir(d):
#             for i in os.listdir(d):
#                 print(i)
#         else:
#             print(d,"is not a valid directory")

# def pause():
#     input("Mani's Magical CLI(Shell) Operations are paused, press 'Enter' to continue the operations further---> ")
#     return

# def echo(comment):
#     echoComment = comment.split()
#     if comment[-1]==">":
#         echoComment = comment[:-1].split()
#         echoComment = " ".join(echoComment)+"\n"
#         l = []
#         l.append(echoComment)
#         return l
#     else:
#         print(" ".join(echoComment)+"\n")

# def environ(inp=0):
#     en = os.environ
#     if inp == ">":
#         l=[]
#         l.append("\n")
#         for i in en:
#             l.append(en[i])
#         return l
#     for i in en:
#         print(en[i])

# def runner(args):
#     if args[-1] == "&":
#         subProcess.Popen(args[:-1])
#     if args[-1] == ">":
#         return subProcess.check_output(args).decode('ascii').split("\n")
#     else:
#         lines = subProcess.check_output(args).decode('ascii').split("\n")
#         for line in lines:
#             print(line)

# def commands(args):
#     commands_List = ["cd", "clr", "dir", "environ", "echo", "help", "pause", "ls"]
#     commands_List_Methods = [cd, clr, directory, environ, echo, helpCommand, pause, ls]
#     try:
#         if args[-1] == "&":
#             if args[0] in commands_List:
#                 args = args[:-1]
#                 if len(args)>1 or args[0] == "cd":
#                     ad = commands_List.index(args[0])
#                     subProcess.call(commands_List_Methods[ad](" ".join(args[1:])))
#                 else:
#                     ad = commands_List.index(args[0])
#                     subProcess.call(commands_List_Methods[ad]())
#             else:
#                 runner(args)
#         elif ">>" in args:
#             redirectionToken(args)
#             return
#         elif ">" in args:
#             redirectionCharacter(args)
#             return
#         elif len(args) == 0:
#             pass
#         elif args[0] == "quit":
#             quit()
#         elif args[0] in commands_List:
#             if len(args)>1 or args[0] == "cd":
#                 ad = commands_List.index(args[0])
#                 commands_List_Methods[ad](" ".join(args[1:]))
#             else:
#                 ad = commands_List.index(args[0])
#                 commands_List_Methods[ad]()
#         else:
#             runner(args)
#     except:
#         print("")


# def redirectionCharacter(args):
#     commands_List = ["cd", "clr", "dir", "environ", "echo", "help", "pause", "ls"]
#     commands_List_Methods = [cd, clr, directory, environ, echo, helpCommand, pause, ls]
#     outputfile = args.index(">") + 1
#     with open(args[outputfile],"w") as f:
#         if args[0] not in commands_List:
#             for i in runner(args[:outputfile]):
#                 f.write(i+"\n")
#         else:
#             if len(args[:outputfile])>1 or args[0] == "cd":
#                 ad = commands_List.index(args[0])
#                 x = commands_List_Methods[ad](" ".join(args[:outputfile][1:]))
#                 for i in x:
#                     f.write(i + "\n")


# def redirectionToken(args):
#     commands_List = ["cd", "clr", "dir", "environ", "echo", "help", "pause", "ls"]
#     commands_List_Methods = [cd, clr, directory, environ, echo, helpCommand, pause, ls]
#     a = args.index(">>")
#     outputfile =  a + 1
#     com = args[:a]
#     com.append(">")
#     with open(args[outputfile],"a") as f:
#         if args[0] not in commands_List:
#             for i in runner(com):
#                 f.write(i+"\n")
#         else:
#             if len(com) > 1 or args[0] == "cd":
#                 ad = commands_List.index(args[0])
#                 x = commands_List_Methods[ad](" ".join(com[1:]))
#                 for i in x:
#                     f.write(i+"\n")


# def main():
#     welcome_message = ("\nWelcome to Mani's Magical CLI(shell)\n"
#                        "\nYou can use help command to check list of all commands and their inputs/behaviors that are supported by Mani's Magical CLI(Shell)\n"
#                        "\nBelow are the list of commands that are supported by Mani's Magical CLI(shell): \n 1.cd <directory>\n 2.clr \n 3.dir <directory>\n 4.ls \n 5.environ \n 6.echo <comment>\n 7.help \n 8.pause \n 9.quit\n"
#                        "\nEnter the Command you would like to execute in the Mani's Magical CLI(Shell):\n")
#     print(welcome_message)
#     commands_List = ["cd", "clr", "dir", "environ", "echo", "help", "pause", "ls","quit"]
#     while True:
#         command = input(os.getcwd() + " --> ").strip()
#         commandSplit = command.split()
#         if commandSplit[0] in commands_List:
#             commands(commandSplit)
#         else:
#             print("'"+command+"' is not recognized as an internal or external command")


if __name__ == "__main__":
        main()
