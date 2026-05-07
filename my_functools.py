import subprocess
import time


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
    do_command(f"tee {file}", inp=text)


def sudo_heartbeat():
    do_command("-v")


def logg(func):
    def wrapper(*args, **kwargs):
        print('==============================')
        print(f'start {func.__name__}()')
        original_result = func(*args, **kwargs)
        print(f'stop {func.__name__}()')
        time.sleep(5)
        return original_result

    return wrapper
