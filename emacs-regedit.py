"""This is a tool for emacs registry key edit."""
import json
import os
import sys
import winreg


def getKey(bits=64):
    """Get key name and value and return a dictionary."""
    key_dict = {}

    if bits == 32:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\GNU\Emacs")
        key_dict['_version'] = '32 bits'
    else:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\GNU\Emacs")
        key_dict['_version'] = '64 bits'

    count = winreg.QueryInfoKey(key)[1]
    for i in range(count):
        name, value, _ = winreg.EnumValue(key, i)
        key_dict[name] = value

    winreg.CloseKey(key)
    return key_dict


def setKey(key_dict, bits=64):
    """Set key name and value."""
    if bits == 32:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\GNU\Emacs", 0, winreg.KEY_WRITE)
    else:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\GNU\Emacs", 0, winreg.KEY_WRITE)
        
    for name, value in key_dict.items():
        if name[0] != '_':
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)
        else:
            try:
                winreg.DeleteValue(key, name[1:])
            except Exception:
                continue

    winreg.CloseKey(key)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        str_json_file = r"{}\regedit_value.json".format(os.getcwd())
        if sys.argv[1] == '--get':
            regedit_json = open(str_json_file, 'wt')
            json.dump([getKey(32), getKey(64)], regedit_json, indent=2)
            regedit_json.close()
            print("Registry keys and values are stored in {}".format(str_json_file))
        elif sys.argv[1] == '--set32':
            regedit_json = open(str_json_file, 'rt')
            bits_list = json.load(regedit_json)
            regedit_json.close()
            for bit in bits_list:
                if bit['_version'] == '32 bits':
                    setKey(bit, 32)
                    break

            print("Set 32 bits registry key done.")

        elif sys.argv[1] == '--set64':
            regedit_json = open(str_json_file, 'rt')
            bits_list = json.load(regedit_json)
            regedit_json.close()
            for bit in bits_list:
                if bit['_version'] == '64 bits':
                    setKey(bit, 64)
                    break

            print("Set 64 bits registry key done.")
        else:
            print("You should use like \"emacs-regedit --get\" or \"emacs-regedit --set32\ or \"emacs-regedit --set64\".")
    else:
        print("You should use like \"emacs-regedit --get\" or \"emacs-regedit --set32\ or \"emacs-regedit --set64\".")
