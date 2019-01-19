import re
a = "123"
b = "123"
is_num = re.match(r"\d+$",a)
is_num_1 = re.match(r"\d+$",b)
if is_num and is_num_1:
    print 1
