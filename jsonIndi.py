import pandas as pd
import json
import numpy as np

def toJson(df):

    df = df.set_index('openTime')

    dic = {}
    for column in df:
        dic[column] = []

    for i, row in df.iterrows() :
        l = row.to_dict()
        
        for val in l:
            k={
                "time" : i / 1000,
                "value" : str(l[val])
            }
            dic[val].append(k)


    return dic
    # json_object = json.dumps(dic, indent = 4)  
    # return json_object