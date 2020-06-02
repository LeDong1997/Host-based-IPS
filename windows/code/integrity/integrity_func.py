from datetime import datetime
import hashlib
from windows.code.database.integrity_db_func import *


# Calculate the hash value
def hash_file(path_file, result):
    try:
        with open(path_file, 'rb') as f_in:
            while True:
                data_block = f_in.read(DATA_BLOCK_SIZE)
                if not data_block:
                    break
                result.update(data_block)
        return result.hexdigest()
    except (Exception, ValueError):
        print(HASH_FILE_ERROR_MSG)
        return ERROR_CODE


# Generate hash string (SHA1) for file
# return hash value (string) or ERROR_CODE
def hash_sha1(path_file):
    result_sha1 = hashlib.sha1()
    result = hash_file(path_file, result_sha1)
    if result == ERROR_CODE:
        return result, "Can't caculate hash file."
    else:
        return SUCCESS_CODE, result


# Generate hash string (SHA-256) for file
# return hash value (string) or ERROR_CODE
def hash_sha256(path_file):
    result_sha256 = hashlib.sha256()
    result = hash_file(path_file, result_sha256)
    if result == ERROR_CODE:
        return result, "Can't caculate hash file."
    else:
        return SUCCESS_CODE, result


def scan_file(path_file):
    current_time = datetime.now()
    current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    print('### \nStarting check integrity for file ...')

    check_object = is_sys_check_object_exist(path_file, FILE_TYPE)
    if check_object is None or check_object == ERROR_CODE:
        print("The file is not in check list.")
        return ERROR_CODE

    # Check file exist
    is_file = check_file_exist(FILE_TYPE, path_file)
    if is_file == FILE_NOT_FOUND_CODE:
        # File remove in system, but exist in check list
        hash_record = get_hash_record_db(FILE_TYPE, path_file)
        if hash_record == ERROR_CODE:
            return ERROR_CODE
        else:
            # Exist info of sys_check_object
            if hash_record is not None:
                id_object = hash_record[0]
                result = del_hash_record_by_id(FILE_TYPE, id_object)
                if result == ERROR_CODE:
                    return ERROR_CODE
            # Remove sys_check_object in list
            result = remove_sys_check_object(path_file, FILE_TYPE)
            if result == ERROR_CODE:
                return ERROR_CODE
            # Insert FILE_DEL_MSG to alert
            result = insert_alert_integrity(current_time, DELETE_FILE_MSG, path_file)
            if result == ERROR_CODE:
                return ERROR_CODE
        return SUCCESS_CODE

    # Case: File exist
    hash_record = get_hash_record_db(FILE_TYPE, path_file)
    if hash_record == ERROR_CODE:
        return ERROR_CODE

    result, hash_str = hash_sha256(path_file)
    # if result ==




def scan_dir(path_dir):
    current_time = datetime.now()
    current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    print('### \nStarting check integrity for dir ...')


# Scan integrity for each system object in list object
def scan_integrity(path_object, type_object):
    if type_object == FILE_TYPE or str(type_object) == str(FILE_TYPE):
        result = scan_file(path_object)
        error_msg = ''
        if result == ERROR_CODE:
            error_msg = 'The file was not in check list.'
        return result, error_msg
    elif type_object == DIR_TYPE or str(type_object) == str(DIR_TYPE):
        result = scan_dir(path_object)
        error_msg = ''
        if result == ERROR_CODE:
            error_msg = 'The folder was not in check list.'
        return result, error_msg


# Validate insert system integrity_object
def validate_insert_sys_check_object(path_object, type_object):
    # Validate type object
    if type_object == FILE_TYPE:
        result = check_file_exist(type_object, path_object)
        if result == FILE_NOT_FOUND_CODE:
            error_msg = "File don't exist. The sys_check_object invalid."
            return ERROR_CODE, error_msg
    elif type_object == DIR_TYPE:
        result = check_file_exist(type_object, path_object)
        if result == DIR_NOT_FOUND_CODE:
            error_msg = "Directory don't exist. The sys_check_object invalid."
            return ERROR_CODE, error_msg
    else:
        error_msg = "The type object invalid."
        return ERROR_CODE, error_msg
    return SUCCESS_CODE, "OK"


# Validate insert system integrity_object from XML file
def validate_path_sys_check_object(path_file):
    name_file = os.path.basename(path_file)
    ext_file = name_file[-3:]
    if ext_file == SYS_CHECK_OBJECT_XML_FILE or ext_file == SYS_CHECK_OBJECT_CSV_FILE:
        result = check_file_exist(FILE_TYPE, path_file)
        if result == FILE_NOT_FOUND_CODE:
            error_msg = "File " + name_file + " not found."
            return ERROR_CODE, error_msg
        else:
            return SUCCESS_CODE, ext_file
    else:
        error_msg = "The program only support XML or CSV file."
        return ERROR_CODE, error_msg


