import random
import optparse
import subprocess
import re

import psutil


from utils.logger import get_logger
# Create a custom logger
logger = get_logger()


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface",
                      help="Specify the interface of which you want to change the MAC address.")
    parser.add_option("-m", "--mac", dest="new_mac",
                      help="Specify a random MAC address you would like to the interface to use.")
    (options, arguments) = parser.parse_args()
    if not options.interface():
        parser.error("[-] Error: interface not specified, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Error: MAC address not specified, use --help for more info.")
    return options


class MacAddress:
    def __init__(self):
        self.devices_list = self._get_devices_list()
        self.mac_address_regexp = re.compile(r'(?:[0-9a-fA-F]:?){12}')

    @staticmethod
    def _get_devices_list():
        addresses = psutil.net_if_addrs()
        result = {}
        for key, value in addresses.items():
            result[key] = value[-1][1]
        return result

    def get_list_of_active_devices(self):
        logger.debug("Getting a list of devices")
        self.devices_list = self._get_devices_list()
        logger.debug(f"List of devices: {self.devices_list}")
        return self.devices_list

    def get_current_mac_address(self, interface_name):
        self.devices_list = self._get_devices_list()
        mac_address = self.devices_list[interface_name]
        logger.debug(f"Current mac address for '{interface_name}' is '{mac_address}'")
        return mac_address

    def get_permanent_address(self, interface_name):
        logger.debug(f"Getting permanent address for: {interface_name}")
        result = subprocess.check_output(["ethtool", "-P", interface_name])
        result = str(result)
        mac_address = re.findall(self.mac_address_regexp, result)[0]
        logger.debug(f"Permanent mac address for '{interface_name}' is '{mac_address}'")
        return mac_address

    @staticmethod
    def _generate_random_mac_address():
        logger.debug("Generating random mac address")
        generated_mac_address = "%02x:%02x:%02x:%02x:%02x:%02x" % (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
        logger.debug(f"Randomly generated address is: {generated_mac_address}")
        return generated_mac_address

    def set_random_mac_address_to_interface(self, interface):
        new_random_mac_address = self._generate_random_mac_address()
        self.change_mac(interface=interface, new_mac=new_random_mac_address)

    @staticmethod
    def change_mac(interface, new_mac):
        logger.debug("[+] Changing MAC address for " + interface + " to " + new_mac)
        subprocess.call(["sudo", "ifconfig", interface, "down"])
        subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
        subprocess.call(["sudo", "ifconfig", interface, "up"])
        subprocess.call(["sudo", "service", "network-manager", "restart"])


def main():

    # real = "a0:1d:48:ac:98:e8"  # enp2s0
    real = "28:e3:47:2c:9f:a3"  # wlo1
    not_real = "02:a0:04:d3:00:11"
    new_mac = not_real
    mac_address = MacAddress()
    # working_interface = "enp2s0"
    working_interface = "wlo1"

    print(mac_address.get_current_mac_address(working_interface))
    mac_address.set_random_mac_address_to_interface(interface=working_interface)
    print(mac_address.get_current_mac_address(working_interface))
    # print(mac_address.get_permanent_address(interface_name=working_interface))
    return
    # print(mac_address.get_list_of_active_devices())
    mac_address.change_mac(working_interface, new_mac)
    print(mac_address.get_current_mac_address(working_interface))
    # print(mac_address.get_list_of_active_devices())
    # print(mac_address.get_current_mac("eth0"))


if __name__ == '__main__':
    main()
