import subprocess
import random
import argparse
import re

def Get_arguments():
    parser = argparse.ArgumentParser(description='Change MAC address.')
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to change MAC address.")
    parser.add_argument("-m", "--mac", dest="new_MAC_Address", help="New MAC address.")
    parser.add_argument("-rd", "--random", dest="Random_MAC", help="create random MAC Address. Type 'y' to use")
    args = parser.parse_args()
    if not args.interface:
        parser.error("[-] Pls enter an interface, use -h for more info")
    elif not args.new_MAC_Address and not args.Random_MAC == 'y':
        parser.error("[-] Pls enter an MAC address, use -h for more info")
    else:
        return args

def Change_MAC_address(interface, new_mac, random_mac):
    if random_mac == 'y':
        mac_a = "00:" + str(random.randint(10, 99)) + ":" + str(random.randint(10, 99)) + ":" + str(
            random.randint(10, 99)) + ":" + str(random.randint(10, 99)) + ":" + str(random.randint(10, 99))
    else:
        mac_a = new_mac
    print("[+] Your new MAC address is: " + mac_a)
    print("[+] Changing MAC address for " + interface + " to " + mac_a)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac_a])
    subprocess.call(["ifconfig", interface, "up"])
    current_mac = Get_current_MAC_address(interface)
    if current_mac == mac_a:
        print("[+] Your " + interface + " MAC address has been changed successfully to " + current_mac)
    else:
        print("[-] Something went wrong. Cant change the MAC address.")

def Get_current_MAC_address(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_address_search_result:
        return mac_address_search_result.group(0)
        # print(mac_address_search_result.group(0))
    else:
        print("[-] Could not read MAC address.")
###### Call #####

args = Get_arguments()
Change_MAC_address(args.interface, args.new_MAC_Address, args.Random_MAC)
