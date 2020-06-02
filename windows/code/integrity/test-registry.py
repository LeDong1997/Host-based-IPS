# import winreg
#
# # Connect key in registry
# access_registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
# key = r"SOFTWARE\Microsoft\Windows\CurrentVersion"
# access_key = winreg.OpenKey(access_registry, key)
# for n in range(20):
#     try:
#         key_name = winreg.EnumKey(access_key, n)
#         access_sub_key = winreg.OpenKey(access_key, key_name)
#         val = winreg.QueryValueEx(access_sub_key, "DisplayName")
#         print(val)
#     except Exception as e:
#         print(e)


from winreg import *

registry = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
def openRegistryA():

    rawKeyA = OpenKey(registry, "SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System")

    try:
        i = 0
        while 1:
            name, value, type = EnumValue(rawKeyA, i)
            print("So i = ", i, name, value, type)
            i += 1

    except WindowsError:
        print("END")

    CloseKey(rawKeyA)

def openRegistryB(name):
    rawKeyB = OpenKey(registry, name)

    try:
        sub_key_count, values_count, last_modified = QueryInfoKey(rawKeyB)
        for i in range(sub_key_count):
            sub_key_name = EnumKey(rawKeyB, i)
            print(sub_key_name)

    except WindowsError:
        print("END")

    CloseKey(rawKeyB)


# openRegistryA()
# openRegistryB(r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System")


# import datetime
# import time
# import winreg
#
#
# # https://stackoverflow.com/questions/6161776/convert-windows-filetime-to-second-in-unix-linux
# def windows_ticks_to_unix_seconds(windows_ticks):
#     return windows_ticks/10000000 - 11644473600
#
# key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
#                      r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\UIPI\Clipboard\ExceptionFormats")
#
# reg_win_ts = winreg.QueryInfoKey(key)[2]  # 100’s of nanoseconds since 1601/01/01.
# print(f'reg_win_ts: {reg_win_ts}')
#
# reg_key_ts = windows_ticks_to_unix_seconds(reg_win_ts)
# print(f'reg_key_ts: {reg_key_ts}')
#
# dt = datetime.datetime.fromtimestamp(reg_key_ts)  # Convert to datatime.
# print(f'dt: {dt}')
# print(f'dt.strftime("%Y-%b-%d"): {dt.strftime("%Y-%b-%d")}')
# print(f'dt.isoformat(): {dt.isoformat()}')
# print(dt.strftime("%Y-%m-%d %H:%M:%S"))


def scan(path_key, indent):
    rawkey = OpenKey(registry, path_key)
    try:
        sub_key_count, values_count, last_modified = QueryInfoKey(rawkey)
        sub_key = OpenKey(registry, path_key)
        print(path_key + "\\")
        for i in range(values_count):
            name, value, type = EnumValue(sub_key, i)
            print("So i = ", i, ' ;ten = ', name, ' ;Gia tri = ', value, ' ;Loai = ', type)
        CloseKey(sub_key)

        for i in range(sub_key_count):
            sub_key_name = EnumKey(rawkey, i)
            path_sub_key = path_key + "\\" + sub_key_name
            scan(path_sub_key, indent + 2)
    except WindowsError:
        print("Loi")
    CloseKey(rawkey)


scan(r"Software\Classes\Directory", 0)

