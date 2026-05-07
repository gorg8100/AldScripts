import subprocess
import time
import datetime


def do_command(command: str, sudo: bool = False, inp: str = None, check_code: bool = True) -> int:
    if sudo:
        command = "sudo " + command
    result = subprocess.run(command, text=True, shell=True, input=inp)
    if check_code and result.returncode != 0:
        raise RuntimeError(f"Command {command} failed, with exit code {result.returncode}")
    return result.returncode


def do_commands(commands: list):
    for command in commands:
        do_command(command)


def write_file(file: str, text: str):
    with open(file, "w") as file:
        file.write(text)


def logg(func):
    def wrapper(*args, **kwargs):
        print('==============================')
        print(f'start {func.__name__}()')
        start_time = time.time()
        original_result = func(*args, **kwargs)
        end_time = time.time()
        print(f'stop {func.__name__}()')
        print("time spent", str(datetime.timedelta(seconds=end_time-start_time)))
        time.sleep(5)
        return original_result

    return wrapper
