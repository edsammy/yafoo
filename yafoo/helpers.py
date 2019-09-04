# yafoo helpers
from datetime import datetime

def get_today_timestamp():
    return round(datetime.timestamp(datetime.today()))

def get_year_timestamp():
    # returns timestamp of January 1, <current_year>
    return round(datetime.timestamp(
        datetime.strptime(
            str(
                datetime.today().year) + '-1-1','%Y-%m-%d'
            )
        )
    )

def more_than_one_line(data):
    if len(data.split('\n')) > 2:
        return 1
    else:
        return 0

def str_data_to_dict(data):
    processed_data = []
    data = data.strip().split('\n')
    headers = data[0].split(',')
    for d in data[1:]:
        entry_dict = {}
        entry_split = d.split(',')
        for h in range(0, len(headers)):
            entry_dict.update({headers[h]:entry_split[h]})
        processed_data.append(entry_dict)
    return processed_data

def sort_by_date(data):
    return sorted(
        data, key=lambda val:datetime.strptime(val['Date'],'%Y-%m-%d')
    )