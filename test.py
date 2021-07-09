import pandas as pd
from indis.hccp import getHCCP
import getData
import json
import numpy as np
from flask import jsonify
from jsonIndi import toJson

if __name__ == "__main__":
    df = (pd.read_csv('test/testData.csv')).drop('Unnamed: 0',axis=1)  

    hccpData = getHCCP(df)

    hccpData = hccpData.drop(['open', 'high', 'low', 'close', 'volume', 'closeTime'],axis=1)

    # print(hccpData)
    print(toJson(hccpData))
    toJson(hccpData)

