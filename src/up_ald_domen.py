from my_functools import (do_command,
                          do_commands,
                          write_file,
                          logg)
from ald_domen_settings import *
from general_commands import (stop_network_manager,
                              write_network_interfaces,
                              restart_and_switch_networking,
                              write_resolv,
                              write_apt_sources,
                              write_apt_aldpro_list,
                              apt_update,
                              reboot,
                              set_hostname,
                              restart_networking)

FULL_HOSTNAME = HOSTNAME + "." + DOMAIN


@logg
def write_hosts():
    text = f"""
{ADDRESS} {FULL_HOSTNAME} {HOSTNAME}
127.0.0.1 localhost.localdomain localhost
"""
    write_file("/etc/hosts", text)


@logg
def write_package_priority():
    text = """
Package: *
Pin: release n=generic
Pin-Priority: 900
    """
    write_file("/etc/apt/preferences.d/aldpro", text)


@logg
def stop_avahi():
    do_commands(["systemctl stop avahi-daemon.service",
                 "systemctl stop avahi-daemon.socket",
                 "systemctl disable avahi-daemon.service",
                 "systemctl disable avahi-daemon.socket"])


@logg
def download_ald():
    do_command("DEBIAN_FRONTEND=noninteractive apt-get install -y -q aldpro-mp")


@logg
def error_checking_download_ald():
    print("Check for errors when downloading")
    if do_command("grep 'error:' /var/log/apt/term.log", check_code=False) == 0:
        raise RuntimeError("An error occurred while downloading ald pro packages")


@logg
def write_resolv_local_dns():
    text = f"""
nameserver 127.0.0.1
search {DOMAIN}
    """
    write_file("/etc/resolv.conf", text)


@logg
def server_promotion():
    do_command(f"aldpro-server-install -d {DOMAIN} -n {HOSTNAME} --ip {ADDRESS} --no-reboot", inp=PASSWORD)


def main():
    stop_network_manager()
    write_network_interfaces(ADDRESS, NETMASK, GATEWAY)
    restart_and_switch_networking()
    write_resolv(DNS, DOMAIN)
    write_hosts()
    set_hostname(FULL_HOSTNAME)

    write_apt_sources()
    write_apt_aldpro_list()
    write_package_priority()
    apt_update()

    stop_avahi()

    download_ald()
    error_checking_download_ald()
    write_resolv_local_dns()
    restart_networking()
    server_promotion()
    reboot()
    return


if __name__ == "__main__":
    main()
