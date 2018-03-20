import re

file_name = 'which capitals % are not major cities ?'
file_name = re.sub("[?,$%^*(+\"\']+", "", file_name)
print(file_name)