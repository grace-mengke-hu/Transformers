import re
import pandas as pd
import rules

test_text = "He has HRR but not CHEK2."

HRR_pattern = rules.HRR_pattern
# 1st method test: directly use regex to search
x = re.search(HRR_pattern, test_text)
print("Regex search 1st match:", x.span(), x.group())  # span is a tuple; group is the part of the string where there was a match
x_all = re.finditer(HRR_pattern, test_text)
print("Regex search all:")
for obj in x_all:
    print(obj.span(), obj.group())

# 2nd method test: use regex object re.compile
HRR_regex = re.compile(HRR_pattern)
y = HRR_regex.search(test_text)
print("Regex object:", y.span(), y.group())
y_all = HRR_regex.finditer(test_text)
print("Regex object match all:")
for obj in y_all:
    print(obj.span(), obj.group())

# 3rd method test: use string match in dataframe
d = {"text": [test_text]}
df = pd.DataFrame(data=d)
print(df)
z = df.text.str.match(HRR_pattern)
print('Data Frame String Match:', z)