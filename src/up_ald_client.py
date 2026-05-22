from my_functools import (do_command,
                          write_file,
                          logg,
                          mkdir_p)
from ald_client_settings import *
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
def restart_network_manager():
    do_command("systemctl restart NetworkManager")


@logg
def write_network_manager_conf_d():
    mkdir_p("/etc/NetworkManager/conf.d")
    text = """
[main]
dns=none
    """
    write_file("/etc/NetworkManager/conf.d/settings.conf", text)


@logg
def write_hosts():
    text = f"""
127.0.0.1       localhost.localdomain localhost
127.0.1.1       {FULL_HOSTNAME} {HOSTNAME}

::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
    """
    write_file("/etc/hosts", text)


@logg
def download_ald():
    do_command("DEBIAN_FRONTEND=noninteractive apt-get install -y -q aldpro-client")


@logg
def domain_entry():
    orgunits_param = "--orgunits \"\""
    if ORGUNITS != "":
        orgunits_param = f"--orgunits {ORGUNITS}"
    do_command(
        f"aldpro-client-installer --guiless --validate --domain {DOMAIN} --account {DOMAIN_USER} --host {HOSTNAME} {orgunits_param}",
        inp=DOMAIN_USER_PASSWORD)


def main():
    if STATIC_ADDRESS:
        if STOP_NETWORK_MANAGER:
            stop_network_manager()
        write_network_interfaces(ADDRESS, NETMASK, GATEWAY)
        restart_and_switch_networking()
    else:
        write_network_manager_conf_d()
        restart_network_manager()
    write_resolv(DOMAIN_ADDRESS, DOMAIN)
    write_hosts()
    set_hostname(FULL_HOSTNAME)

    if STATIC_ADDRESS:
        restart_networking()
    else:
        restart_network_manager()

    write_apt_sources()
    write_apt_aldpro_list()
    apt_update()

    download_ald()
    domain_entry()
    reboot()
    return


if __name__ == "__main__":
    main()
