#!/usr/env python3

import pandas as pd
import openpyxl
import ruamel.yaml as yaml


with open("template.yaml") as fin:
    template = yaml.safe_load(fin)

print(template)

#df = pd.DataFrame.from_dict([dic for dic in template.values()])

df = pd.DataFrame(template)
df.to_excel("template.xlsx")
print(df.head())

print("---")
df = pd.DataFrame({"SAMPLE_NAME_GPCF": ["a description", "a example"],
                   "PROJECT": ["another description", "another example"]},
                  index=["description", "example"])
json_Data = df.to_dict()
print(json_Data)
with open("example.yaml", "w") as fout:
    yaml.safe_dump(json_Data, fout, allow_unicode=True)

print(pd.DataFrame.from_dict(json_Data))

#EOF