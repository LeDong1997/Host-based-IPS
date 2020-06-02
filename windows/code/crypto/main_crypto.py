import sys
from .crypto_func import *


def usage_crypto_func():
    print("\nAdd argument to crypto function.")
    print("$ python demo_crypto.py -operation -object -path -password [options]")
    print("\t--operation: choice encryption [-e] / decryption [-d]")
    print("\t--object: choice file [-f] / directory [-d]")
    print("\t--path: path of file / directory")
    print("\t--password: choice password use encrypt / decrypt")
    print("\t[--option]: the default CONFIRM_DEL [0] / SKIP [1] / OVERRIDE [2]")
    print("Example:\n$ python demo_crypto.py -e -f \"C:\\test.txt\" \"abc\"")
    print("$ python demo_crypto.py -d -d \"C:\\test\" \"abc\" 1")
    return 0


def main_crypto():
    try:
        argv = sys.argv
        argc = len(argv)
        if argc == 5 and argv[1] == '-e':           # Encryption
            if argv[2] == '-f':
                return encrypt_file(argv[3], argv[4])
            elif argv[2] == '-d':
                return encrypt_dir(argv[3], argv[4])
            else:
                return usage_crypto_func()
        elif argc == 6 and argv[1] == '-d':           # Decryption
            choice = int(argv[5])
            if argv[2] == '-f':
                if choice == CONFIRM_DEL:               # Choice SKIP or OVERRIDE ?
                    return decrypt_file(argv[3], argv[4], CONFIRM_DEL)
                elif choice == SKIP_CODE or choice == OVERRIDE_CODE:
                    return decrypt_file(argv[3], argv[4], choice)
                else:
                    return usage_crypto_func()
            elif argv[2] == '-d':
                if choice == SKIP_CODE or choice == OVERRIDE_CODE:
                    return decrypt_dir(argv[3], argv[4], choice)
                else:
                    return usage_crypto_func()
            else:
                return usage_crypto_func()
        else:
            return usage_crypto_func()
    except(Exception, ValueError):
        print("Error in call function.")
        return -1
