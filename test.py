from utils import get_process_by_name
from Win32Wrapper import Win32Wrapper
import psutil

PROGRAM_NAME = 'hadesstar.exe'
WINDOW_TITLE = "Hades' Star"
test = 'Device Manager'


class ProgramController:
    def __init__(self, program_name, window_title, window_id):
        try:
            self.program = self.get_program(program_name)
            print('initiating win rapper')
            self.window = Win32Wrapper(window_title)
            self.options = {
                '0': ('quit', lambda: None),
                '1': ('start preview', self.window.video),

            }
            self.run()
        except Exception as e:
            print(e)

    def run(self):
        while True:
            val = self.control()
            if val == self.options['0']:
                break

    def control(self):
        for key, val in self.options.items():
            print(key, val)
        command = input('Please choose option: ')
        if command in self.options:
            self.options[command][1]()
        else:
            print("you chose an invalid option.")

    def get_program(self, program_name):
        program = get_process_by_name(program_name)
        if not type(program) == psutil.Process:
            raise Exception("Program not found")
        else:
            print("program FOUND")
            return program
ProgramController(PROGRAM_NAME,WINDOW_TITLE,0)