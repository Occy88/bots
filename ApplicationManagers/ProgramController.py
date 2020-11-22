from ApplicationManagers.utils import get_process_by_name

try:
    from ApplicationManagers.Win32Wrapper import Win32Wrapper as program
except Exception as e:
    print("NOT WINDOWS, ASSUMING ADB.")
    from ApplicationManagers.ADBManager import AdbWrapper as program
import psutil

PROGRAM_NAME = 'scrcpy.exe'
program_TITLE = "SM-G9650"
test = 'Device Manager'


class ProgramController:
    def __init__(self, program_title):
        print('initiating program')
        self.program = program(program_title)
        self.options = {
            '0': ('quit', lambda: None),
            '1': ('start preview', self.program.start_capture),

        }

    def run(self):
        while True:
            val = self.control()
            if val == self.options['0']:
                break

    def control(self):
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

# ProgramController(PROGRAM_NAME,program_TITLE,0)
