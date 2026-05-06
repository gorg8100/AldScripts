from my_functools import *
from ald_domen_settings import *

FULL_HOSTNAME = HOSTNAME + "." + DOMAIN


@logg
def stop_network_manager():
    do_commands(["systemctl stop NetworkManager",
                 "systemctl disable NetworkManager",
                 "systemctl mask NetworkManager"])


@logg
def write_network_interfaces():
    text = f"""
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
   address {ADDRESS}
   netmask {NETMASK}
   gateway {GATEWAY}
    """
    write_file("/etc/network/interfaces", text)


@logg
def restart_and_switch_networking():
    do_commands(["ip addr flush dev eth0",
                 "systemctl restart networking"])


@logg
def write_resolv():
    text = f"""
nameserver {DNS}
search {DOMAIN}
    """
    write_file("/etc/resolv.conf", text)


@logg
def write_hosts():
    text = f"""
{ADDRESS} {FULL_HOSTNAME} {HOSTNAME}
127.0.0.1 localhost.localdomain localhost
"""
    write_file("/etc/hosts", text)


@logg
def set_hostname():
    do_command(f"hostnamectl set-hostname {FULL_HOSTNAME}")


@logg
def write_apt_sources():
    text = f"""
deb https://dl.astralinux.ru/astra/frozen/1.7_x86-64/1.7.9/uu/1/repository-main 1.7_x86-64 main non-free contrib
deb https://dl.astralinux.ru/astra/frozen/1.7_x86-64/1.7.9/uu/1/repository-update 1.7_x86-64 main contrib non-free
"""
    write_file("/etc/apt/sources.list", text)


@logg
def write_apt_aldpro_list():
    text = "deb https://dl.astralinux.ru/aldpro/frozen/01/3.2.0 1.7_x86-64 main base"
    write_file("/etc/apt/sources.list.d/aldpro.list", text)


@logg
def write_package_priority():
    text = """
Package: *
Pin: release n=generic
Pin-Priority: 900
    """
    write_file("/etc/apt/preferences.d/aldpro", text)


@logg
def apt_update():
    do_commands(["apt update",
                 "apt list --upgradable",
                 "apt dist-upgrade -y -o Dpkg::Options::=--force-confnew"])


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
    print("Проверка на ошибки при скачивании.")
    do_command("grep 'error:' /var/log/apt/term.log", check_code=False)


@logg
def write_resolv_local_dns():
    text = f"""
nameserver 127.0.0.1
search {DOMAIN}
    """
    write_file("/etc/resolv.conf", text)


@logg
def restart_networking():
    do_command("systemctl restart networking")


@logg
def server_promotion():
    do_command(f"aldpro-server-install -d {DOMAIN} -n {HOSTNAME} --ip {ADDRESS} --no-reboot -p {PASSWORD}")


@logg
def reboot():
    do_command("reboot")


def main():
    sudo_heartbeat()
    stop_network_manager()
    write_network_interfaces()
    restart_and_switch_networking()
    write_resolv()
    write_hosts()
    set_hostname()
    write_apt_sources()
    write_apt_aldpro_list()
    write_package_priority()
    sudo_heartbeat()
    apt_update()
    stop_avahi()
    sudo_heartbeat()
    download_ald()
    error_checking_download_ald()
    write_resolv_local_dns()
    restart_networking()
    sudo_heartbeat()
    server_promotion()
    reboot()
    return


if __name__ == "__main__":
    main()
