#!/usr/bin/env python3

import os
import sys

from trezorlib.client import TrezorClient
from trezorlib.ui import ClickUI

from trezor_encrypter import EncryptionSession, trezor_encrypt_dir, wait_for_devices, choose_device, trezor_decrypt_dir

help_text = """
Usage: trezorenc COMMAND [OPTIONS]

Options:
  -d DIRECTORY  Specify directory to perform encryption/decryption. Defaults to present directory.

Commands:
  help          Display help message.
  interactive   Run program in interactive mode.
  encrypt       Encrypt directory.
  decrypt       Decrypt directory.
""".strip()


def main():
    args = sys.argv[1:]

    # Poor-man's command line argument parsing
    if len(args) > 1:
        if args[1] == '-d':
            if len(args) > 2:
                directory = args[2]
            else:
                print('Missing directory')
                return
        else:
            print(f'Unknown option "{args[1]}"')
            return
    else:
        directory = os.getcwd()

    if args[0] == 'help':
        print(help_text)
    elif args[0] == 'interactive':
        session = EncryptionSession(directory)
        session.run_menu()
    elif args[0] == 'encrypt':
        devices = wait_for_devices()
        transport = choose_device(devices)
        c = TrezorClient(transport, ui=ClickUI())
        trezor_encrypt_dir(c, directory)
    elif args[0] == 'decrypt':
        print('decrypting')
        devices = wait_for_devices()
        transport = choose_device(devices)
        c = TrezorClient(transport, ui=ClickUI())
        trezor_decrypt_dir(c, directory)


if __name__ == '__main__':
    main()
