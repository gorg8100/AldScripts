import subprocess


def do_command(command: str, sudo: bool = True):
    if sudo:
        command = "sudo " + command
    result = subprocess.run(command)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError(f"Command {command} failed, with exit code {result.returncode}")


def do_commands(commands: list[str]):
    for command in commands:
        do_command(command)


def write_file(file: str, text: str):
    do_command(f"echo '{text}' > {file}")


def sudo_heartbeat():
    do_command("-v")
