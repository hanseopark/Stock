import pandas as pd
import requests
import re
import json


def _parse_json(url, headers = {'User-agent': 'Mozilla/5.0'}):
    html = requests.get(url=url, headers = headers).text
    json_str = html.split('root.App.main =')[1].split('(this)')[0].split(';\n}')[0].strip()

    try:
        data = json.loads(json_str)[
            'context']['dispatcher']['stores']['QuoteSummaryStore']
    except:
        return '{}'
    else:
        # return data
        new_data = json.dumps(data).replace('{}', 'null')
        new_data = re.sub(r'\{[\'|\"]raw[\'|\"]:(.*?),(.*?)\}', r'\1', new_data)

        json_info = json.loads(new_data)

        return json_info



def _parse_table(json_info):
    df = pd.DataFrame(json_info)

    if df.empty:
        return df

    del df["maxAge"]

    df.set_index("endDate", inplace=True)
    df.index = pd.to_datetime(df.index, unit="s")

    df = df.transpose()
    df.index.name = "Breakdown"

    return df

ticker='GE'
url = 'https://finance.yahoo.com/quote/'+ticker+'/financials?p='+ticker
json_info = _parse_json(url)

temp = json_info["incomeStatementHistory"]["incomeStatementHistory"]

res = _parse_table(temp)

print(res)

#print(data)

#df = pd.read_json(data)
#df = pd.read_json(temp, orient = 'index')
#print(df)

