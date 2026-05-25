import sys
import os

from my_functools import (do_command,
                          logg)
from general_commands import (write_resolv,
                              restart_networking)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from ald_client_settings import *

FULL_HOSTNAME = HOSTNAME + "." + DOMAIN


@logg
def restart_network_manager():
    do_command("systemctl restart NetworkManager")


@logg
def graphic_domain_entry():
    do_command("aldpro-client-installer")


def main():
    write_resolv(DOMAIN_ADDRESS, DOMAIN)

    if STATIC_ADDRESS:
        restart_networking()
    else:
        restart_network_manager()

    graphic_domain_entry()
    return


if __name__ == "__main__":
    main()
