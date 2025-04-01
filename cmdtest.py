import asyncio
import cmd
import sys
import main
from DB import IChroma
from TTS.xhTTs import tts_websocket


class SimpleCLI(cmd.Cmd):
    prompt = "CLI> "  # 设置命令提示符
    intro = "Welcome to the simple CLI. Type help or ? to list commands."

    def do_hello(self, arg):
        "Say hello with an optional name: hello [name]"
        if arg:
            print(f"Hello, {arg}!")
        else:
            print("Hello!")

    def do_exit(self, arg):
        "Exit the CLI"
        print("Goodbye!")
        return True

    def do_echo(self, arg):
        "Echo the input: echo [message]"
        print(arg)

    def do_add(self, arg):
        "Add two numbers: add num1 num2"
        try:
            numbers = list(map(float, arg.split()))
            if len(numbers) != 2:
                print("Usage: add num1 num2")
            else:
                print(f"Result: {numbers[0] + numbers[1]}")
        except ValueError:
            print("Please enter valid numbers.")

    def do_EOF(self, arg):
        "Handle Ctrl+D (EOF) to exit"
        return True
    #问答系统
    def do_spk(self,arg):
        str=main.test()
        print(f"user input is {str['documents'][0]}")

        asyncio.run(tts_websocket(str))
        print(f"user question is {arg}")
    #加载知识库
    def do_load(self,arg):
        print(f"load html is {arg}")

if __name__ == "__main__":
    IChroma.create_client()
    IChroma.init()
    SimpleCLI().cmdloop()
