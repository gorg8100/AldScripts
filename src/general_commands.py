from my_functools import (do_commands,
                          write_file,
                          logg,
                          do_command)


@logg
def stop_network_manager():
    do_commands(["systemctl stop NetworkManager",
                 "systemctl disable NetworkManager",
                 "systemctl mask NetworkManager"])


@logg
def write_network_interfaces(address: str, netmask: str, gateway: str):
    text = f"""
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
   address {address}
   netmask {netmask}
   gateway {gateway}
    """
    write_file("/etc/network/interfaces", text)


@logg
def restart_and_switch_networking():
    do_commands(["ip addr flush dev eth0",
                 "systemctl restart networking"])


@logg
def write_resolv(dns: str, domain: str):
    text = f"""
nameserver {dns}
search {domain}
    """
    write_file("/etc/resolv.conf", text)


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
def apt_update():
    do_commands(["apt update",
                 "apt list --upgradable",
                 "apt dist-upgrade -y -o Dpkg::Options::=--force-confnew"])


@logg
def reboot():
    do_command("reboot")


@logg
def set_hostname(full_hostname: str):
    do_command(f"hostnamectl set-hostname {full_hostname}")


@logg
def restart_networking():
    do_command("systemctl restart networking")
