import os
import time
from windows.code.program_msg import *


# Search all files in directory and sub-directory by name
# Example
# pathScanDir = r"C:\\Users\Cu Lee\Desktop"
# search_file("Dev", pathScanDir)
def search_file(name_file, path_dir):
    # type<list_dir, list_file>: list
    # type<parent_dir>: string
    for parent_dir, list_dir, list_file in os.walk(path_dir):
        for file_obj in list_file:
            if name_file in file_obj:
                print(os.path.join(parent_dir, file_obj))


# Check file or directory exist
# Return FILE_NOT_FOUND_CODE or path object (file, dir)
def check_file_exist(type_obj, path_obj):
    # Check file exist
    if type_obj == FILE_TYPE:
        if os.path.isfile(path_obj):
            return path_obj
        else:
            print("File not exist.")
            return FILE_NOT_FOUND_CODE

    # Check directory exist
    if type_obj == DIR_TYPE:
        if os.path.isdir(path_obj):
            return path_obj
        else:
            print("Directory not exist.")
            return DIR_NOT_FOUND_CODE


# Get last time create/modify/access file
def get_time_file(path_file):
    try:
        time_property = {}
        # Get last create time of file in seconds since epoch
        create_time_second = os.path.getctime(path_file)
        # Convert second to format string
        create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(create_time_second))
        time_property.update({'create_time': create_time})

        # Get last modify time of file in seconds since epoch
        modify_time_second = os.path.getmtime(path_file)
        # Convert second to format string
        modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modify_time_second))
        time_property.update({'modify_time': modify_time})

        # Get last access time of file in seconds since epoch
        access_time_second = os.path.getatime(path_file)
        # Convert second to format string
        access_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(access_time_second))
        time_property.update({'access_time': access_time})
        return time_property
    except (ValueError, Exception):
        return None
