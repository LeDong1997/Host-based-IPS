import struct
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from windows.code.system.file_func import *


# Get password from keyboard
# return password or ERROR_CODE if password invalid
def get_password():
    try_input = 0
    while try_input < 3:
        password = str(input("Enter a password encryption/decryption: "))
        re_password = str(input("Confirm password: "))
        if password == re_password:
            return password
        else:
            print("Password incorrect!")
            try_input += 1
            if try_input == 3:
                print("The password is not valid more than 3 times.")
                return ERROR_CODE


# Generate key from password
# return 32 byte (SHA-256) or ERROR_CODE
def get_key_from_password(password):
    salt = b'bkcs'
    iteration = 4096
    len_key = 32

    # Generate key from password using HMAC-PBKDF2
    try:
        key_hex = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iteration, len_key)
        return key_hex
    except (Exception, ValueError):
        print(GENERATE_KEY_ERROR_MSG)
        return ERROR_CODE


# Handle process encrypt file
# return ERROR_CODE or SUCCESS_CODE
def process_encrypt(path_file, key):
    tmp_path_file, ext_file = os.path.splitext(path_file)
    i = 0

    # a.txt -> a_001.enc
    path_file_enc = tmp_path_file + "_" + '{:03d}'.format(i) + TYPE_ENCRYPT_FILE

    while True:
        if os.path.isfile(path_file_enc):
            i += 1
            path_file_enc = tmp_path_file + "_" + '{:03d}'.format(i) + TYPE_ENCRYPT_FILE
        else:
            break

    file_size = os.path.getsize(path_file)
    iv = Random.new().read(AES.block_size)
    encryption = AES.new(key, AES.MODE_CBC, iv)

    try:
        with open(path_file, 'rb') as f_in:
            with open(path_file_enc, 'wb') as f_out:
                f_out.write(struct.pack('<Q', file_size))
                f_out.write(iv)
                # Pack 16 byte -> encrypt info of old file with AES
                f_out.write(encryption.encrypt(struct.pack('16s', ext_file.encode('utf-8'))))

                # Encrypt file by data block
                while True:
                    data_block = f_in.read(DATA_BLOCK_SIZE)
                    len_block = len(data_block)
                    if len_block == 0:
                        f_in.close()
                        os.remove(path_file)
                        print(ENCRYPT_DIR_SUCCESS_MSG)
                        return SUCCESS_CODE
                    elif len_block % 16 != 0:
                        data_block += b' ' * (16 - len_block % 16)      # padding with spaces
                    f_out.write(encryption.encrypt(data_block))
    except (ValueError, Exception):
        print(ENCRYPT_FILE_ERROR_MSG)
        return ERROR_CODE


# Encrypt a single file
# return ERROR_CODE / SUCCESS_CODE
def encrypt_file(path_file, password):
    result = check_file_exist(0, path_file)
    if result == FILE_NOT_FOUND_CODE:
        return ERROR_CODE

    print('### \nStarting encrypt file ...')
    key_enc = get_key_from_password(password)
    return process_encrypt(path_file, key_enc)


# Handle process decrypt file
# return ERROR_CODE / SUCCESS_CODE
def process_decrypt(path_file, key, choice):
    try:
        with open(path_file, 'rb') as f_in:
            file_size = struct.unpack('<Q', f_in.read(struct.calcsize('Q')))[0]
            iv = f_in.read(AES.block_size)
            decryption = AES.new(key, AES.MODE_CBC, iv)

            #  Unpack 16 byte -> Decrypt info of old file with AES
            pack_ext_old_file = decryption.decrypt(f_in.read(16))
            try:
                ext_old_file = struct.unpack('16s', pack_ext_old_file)[0].decode('utf-8').replace("\x00", "")
            except (Exception, ValueError):
                print(PASSWORD_INCORRECT_MSG)
                # print(DECRYPT_FILE_ERROR_MSG)
                return PASSWORD_INCORRECT_CODE

            # a_001.enc -> a_001.txt
            # Get path file decryption
            temp_path_file, name_file_dec = os.path.split(path_file)
            if len(name_file_dec) > 8:
                path_file_dec = path_file[:-8] + ext_old_file
            else:  # a.enc -> a.txt
                path_file_dec = os.path.splitext(path_file)[0] + ext_old_file

            if os.path.isfile(path_file_dec):
                print(FILE_EXIST_MSG)
                if choice == OVERRIDE_CODE:
                    os.remove(path_file_dec)  # Remove file decryption
                elif choice == SKIP_CODE:
                    print(SKIP_OVERRIDE_MSG)
                    return SKIP_CODE
                else:
                    return CONFIRM_DEL

            # Decrypt file by data block
            with open(path_file_dec, 'wb') as f_out:
                while True:
                    data_block = f_in.read(DATA_BLOCK_SIZE)
                    len_block = len(data_block)
                    if len_block == 0:
                        print(DECRYPT_FILE_SUCCESS_MSG)
                        return SUCCESS_CODE

                    decode_data_block = decryption.decrypt(data_block)
                    n = len(decode_data_block)
                    if file_size > n:
                        f_out.write(decode_data_block)
                    else:
                        f_out.write(decode_data_block[:file_size])  # Remove padding on last block
                    file_size -= n
    except (Exception, ValueError):
        print(DECRYPT_FILE_ERROR_MSG)
        return ERROR_CODE


# Decrypt a single file
# return ERROR_CODE, PASSWORD_INCORRECT_CODE or SUCCESS_CODE
def decrypt_file(path_file, password, choice):
    result = check_file_exist(0, path_file)
    if result == FILE_NOT_FOUND_CODE:
        return ERROR_CODE

    print('### \nStarting decrypt file ...')
    key_dec = get_key_from_password(password)
    result = process_decrypt(path_file, key_dec, choice)
    if result == SUCCESS_CODE:
        os.remove(path_file)
    return result


# Encrypt all file in directory and sub-directory
# return ERROR_CODE or SUCCESS_CODE
def encrypt_dir(path_dir, password):
    result = check_file_exist(1, path_dir)
    if result == DIR_NOT_FOUND_CODE:
        return ERROR_CODE

    print('### \nStarting encrypt directory ...')
    key_enc = get_key_from_password(password)

    # Scan directory
    # type<list_dir, list_file> = list
    # type<parent_dir> = string
    for parent_dir, list_dir, list_file in os.walk(path_dir):
        for file in list_file:
            process_encrypt(key_enc, os.path.join(parent_dir, file))

    print(ENCRYPT_DIR_SUCCESS_MSG)
    return SUCCESS_CODE


# Decrypt all file in directory and sub-directory
def decrypt_dir(path_dir, password, choice):
    result = check_file_exist(1, path_dir)
    if result == DIR_NOT_FOUND_CODE:
        return ERROR_CODE

    print('### \nStarting decrypt directory ...')
    key_dec = get_key_from_password(password)

    # Scan directory
    # type<list_dir, list_files> = list
    # type<parent_dir> = string
    for parent_dir, list_dir, list_file in os.walk(path_dir):
        for file in list_file:
            path_file = os.path.join(parent_dir, file)
            ext_file = os.path.splitext(path_file)
            if ext_file[1] == TYPE_ENCRYPT_FILE:  # ext = ".enc"
                result = process_decrypt(path_file, key_dec, choice)
                if result == PASSWORD_INCORRECT_CODE:
                    # print(PASSWORD_INCORRECT_MSG)
                    return PASSWORD_INCORRECT_CODE
                if result == SUCCESS_CODE:
                    os.remove(path_file)
    print(DECRYPT_DIR_SUCCESS_MSG)
    return SUCCESS_CODE
