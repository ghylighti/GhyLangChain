import asyncio
import cmd
import time
import Controller
from DB import IChroma
from TTS.xhTTs import tts_websocket
from TTS import PyGame


class SimpleCLI(cmd.Cmd):
    prompt = "CLI> "  # 设置命令提示符
    intro = "Welcome to the simple CLI. Type help or ? to list commands."
    role=None
    book=None
    def do_hello(self, arg):
        "Say hello with an optional name: hello [name]"
        if arg:
            print(f"Hello, {arg}!")
        else:
            print("Hello!")
    def do_clean(self,arg):
        IChroma.clean_db()
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
    def do_spk(self, arg):
        print(f"arg:{arg}==>role:{self.role}==>book:{self.book}")
        result=Controller.query(arg,self.role,self.book)
        ans=Controller.get_prompt(arg,result=result,role=self.role,book=self.book)
        asyncio.run(tts_websocket(ans))
        time.sleep(1)  # 等待 0.5 秒再播放，确保文件写入完成
        PyGame.play()
        print(f"user question is {arg}")
    #加载知识库
    def do_load(self,arg):
        Controller.load(arg)
        print(f"load html is {arg}")
    def do_role(self,arg):
        self.role=arg
    def do_book(self,arg):
        self.book=arg
if __name__ == "__main__":
    PyGame.init()
    IChroma.create_client()
    IChroma.init()
    SimpleCLI().cmdloop()
