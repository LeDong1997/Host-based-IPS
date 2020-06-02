import json
import sys
from .integrity_func import *
from .handle_xml_func import *
from .handle_csv_func import *
# from .handle_registry import *


def usage_integrity_func():
    print("\nAdd argument to integrity check function.")
    print("-i [path] [type]: insert check object to database")
    print("-d [path] [type]: insert check object from database")
    print("\t[type]: the file[0] / folder[1] / registry[2]")
    print("Example:\n$ python demo_crypto.py -e -f \"C:\\test.txt\" \"abc\"")
    print("$ python demo_crypto.py -d -d \"C:\\test\" \"abc\" 1")
    return 0


def main_integrity():
    try:
        create_integrity_db()
        argv = sys.argv
        argc = len(argv)

        if argc == 4:
            # Insert sys_check_object to database
            # Example: demo_crypto.py -i "test.txt" file[0] / directory [1]
            if argv[1] == '-i':
                result, error_msg = validate_insert_sys_check_object(argv[2], argv[3])
                if result == SUCCESS_CODE:
                    result = insert_or_update_sys_check_object(argv[2], argv[3])
                    check_list = get_list_sys_check_object()
                    print(json.dumps({'result': result == SUCCESS_CODE, 'check_list': check_list}))
                else:
                    print(json.dumps({'result': result == SUCCESS_CODE, 'error_msg': error_msg}))
            # Remove sys_check_object from database
            # Example: demo_crypto.py -r "test.txt" file[0] / directory [1]
            elif argv[1] == '-r':
                result = remove_sys_check_object(argv[2], argv[3])
                if result == SUCCESS_CODE:
                    check_list = get_list_sys_check_object()
                    print(json.dumps({'result': result == SUCCESS_CODE, 'check_list': check_list}))
                else:
                    print(json.dumps({'result': result == SUCCESS_CODE, 'error_msg': "Error remove sys_check_object"}))
            # Scan integrity for system
            # Example: demo_crypto.py -s "test.txt" file[0] / directory [1] / registry[3]
            elif argv[1] == '-s':
                res, msg = scan_integrity(argv[2], argv[3])
                # alertList = get_alert_list()
                success = res == 0
                if res != 0:
                    print(json.dumps({'result': success, 'error_msg': msg}))
                else:
                    print(json.dumps({'result': success, 'message': msg}))
            return SUCCESS_CODE
        else:
            if argc == 3:
                # Add sys_check_object from XML file
                # Example: demo_crypto.py -x sample.xml
                if argv[1] == '-x':
                    result, msg = validate_path_sys_check_object(argv[2])
                    if result == SUCCESS_CODE:
                        if msg == SYS_CHECK_OBJECT_XML_FILE:
                            result = add_sys_check_object_from_xml(argv[2])
                        elif msg == SYS_CHECK_OBJECT_CSV_FILE:
                            result = add_sys_check_object_from_csv(argv[2])
                        check_list = get_list_sys_check_object()
                        print(json.dumps({'result': result == SUCCESS_CODE, 'check_list': check_list}))
                    else:
                        print(json.dumps({'result': result == SUCCESS_CODE, 'error_msg': msg}))
                # Calculate the hash message (SHA-256) for file
                # Example: demo_crypto.py -m "test.txt"
                if argv[1] == '-m':
                    result = check_file_exist(FILE_TYPE, argv[2])
                    if result == FILE_NOT_FOUND_CODE:
                        print(json.dumps({'result': False, 'error_msg': "Path file invalid."}))
                    else:
                        result, msg = hash_sha256(argv[2])
                        if result == SUCCESS_CODE:
                            print(json.dumps({'result': True, 'hash_str': msg}))
                        else:
                            print(json.dumps({'result': False, 'error_msg': msg}))
                # Get list alert have id gather than id_alert old
                # Example: demo_crypto.py -a id
                if argv[1] == '-a':
                    result = get_list_last_alert_from_id(argv[2])
                    print(json.dumps({'list_alert': result}))
                return SUCCESS_CODE
            if argc == 2:
                # Get list sys_check_object from database
                # Example: demo_crypto.py -l
                if argv[1] == '-l':
                    check_list = get_list_sys_check_object()
                    if check_list == ERROR_CODE:
                        print(json.dumps({'result': False, 'error_msg': "Cannot connect to database."}))
                    else:
                        print(json.dumps({'result': True, 'check_list': check_list}))
                    return SUCCESS_CODE
                # Get list last 1000 alert integrity from database
                # Example: demo_crypto.py -a
                elif argv[1] == '-a':
                    alert_list = get_list_alert_limit_1000()
                    if alert_list == ERROR_CODE:
                        print(json.dumps({'result': False, 'error_msg': "Cannot connect to database."}))
                    else:
                        print(json.dumps({'result': True, 'alert_list': alert_list}))
                    return SUCCESS_CODE
                # Get last alert_id from database
                # Example: demo_crypto.py -e
                elif argv[1] == '-e':
                    id_alert = get_last_alert_id_integrity()
                    if id_alert == ERROR_CODE:
                        print(json.dumps({'result': False, 'error_msg': "Cannot connect to database."}))
                    else:
                        print(json.dumps({'result': True, 'last_alert_id': id_alert}))
                    return SUCCESS_CODE
                # Get list hash_file from database
                # Example: demo_crypto.py -h
                elif argv[1] == '-h':
                    hash_file_list = get_list_hash_file_limit_1000()
                    if hash_file_list == ERROR_CODE:
                        print(json.dumps({'result': False, 'error_msg': "Cannot connect to database."}))
                    else:
                        print(json.dumps({'result': True, 'hash_file_list': hash_file_list}))
                    return SUCCESS_CODE
                # Get list hash registry from database
                # Example: demo_crypto.py -g
                elif argv[1] == '-g':
                    hash_registry_list = get_list_hash_registry_limit_1000()
                    if hash_registry_list == ERROR_CODE:
                        print(json.dumps({'result': False, 'error_msg': "Cannot connect to database."}))
                    else:
                        print(json.dumps({'result': True, 'hash_registry_list': hash_registry_list}))
                    return SUCCESS_CODE
                else:
                    return usage_integrity_func()
            return usage_integrity_func()
    except(Exception, ValueError):
        print("Error in call function.")
        return -1
