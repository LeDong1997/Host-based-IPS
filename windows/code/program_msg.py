#
# Determine messages and constants used in the file-system-protection module
#
# Determine the size of the encrypt/decrypt data_block
DATA_BLOCK_SIZE = 32768

# Determine the value returned by the function
ERROR_CODE = -1
SUCCESS_CODE = 0

# Define operating system platform
UNKNOWN_PLATFORM = -1
WINDOWS_PLATFORM = 0
LINUX_PLATFORM = 1

# File message
FILE_NOT_FOUND_CODE = -2
DIR_NOT_FOUND_CODE = -3

FILE_EXIST_MSG = 'File exist.'

# Crypto
PASSWORD_INCORRECT_CODE = -4

CONFIRM_DEL = 0
SKIP_CODE = 1
OVERRIDE_CODE = 2

SKIP_OVERRIDE_MSG = 'Skip override file.'

# Determine the messages returned by the crypto function
GENERATE_KEY_ERROR_MSG = 'Error in generate key from password'

# Determine the messages encrypt/decrypt file and directory
PASSWORD_INCORRECT_MSG = 'Error. Password incorrect'
ENCRYPT_FILE_SUCCESS_MSG = 'Done encrypt file.'
ENCRYPT_FILE_ERROR_MSG = '#Error in process encrypt file.'
DECRYPT_FILE_SUCCESS_MSG = 'Done decrypt file.'
DECRYPT_FILE_ERROR_MSG = '#Error in process decrypt file.'
ENCRYPT_DIR_SUCCESS_MSG = 'Done encrypt directory.'
DECRYPT_DIR_SUCCESS_MSG = 'Done decrypt directory.'

# Define format encrypt file
TYPE_ENCRYPT_FILE = ".enc"
#
#
# Determine the error value / messages returned by the database query function
CREATE_DB_ERROR = -4
INSERT_RECORD_ERROR = -5
UPDATE_RECORD_ERROR = -6
DELETE_RECORD_ERROR = -7

CREATE_DB_ERROR_MSG = 'There was an error creating the database.'
CREATE_DB_SUCCESS_MSG = 'Create success database: '

QUERY_TABLE_DB_ERROR_MSG = 'The error connect to database.'

# Hash
HASH_FILE_ERROR_MSG = 'Error in generate hash string for file.'


FILE_TYPE = '0'
DIR_TYPE = '1'
REGISTRY_TYPE = '2'


ADD_FILE_MSG = 'The new file add to folder.'
CHANGE_FILE_MSG = 'File is changed.'
DELETE_FILE_MSG = 'File is deleted.'
NOT_CHANGE_FILE_MSG = 'File isn\'t changed.'


FILE_CHECK_TAG = 'file_check'
FOLDER_CHECK_TAG = 'folder_check'
REGISTRY_CHECK_TAG = 'windows_registry'
CHECK_LIST_TAG = 'check_list'

# New sys_check add to database is value 0
SYS_CHECK_OBJECT_NEW = 0
SYS_CHECK_OBJECT_OLD = 1

SYS_CHECK_OBJECT_IGNORE = 1

SYS_CHECK_OBJECT_XML_FILE = 'xml'
SYS_CHECK_OBJECT_CSV_FILE = 'csv'
