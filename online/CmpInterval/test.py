import re
str = "20112"
if re.match('^[0-9]+$', str):
    print("pass")