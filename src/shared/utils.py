def get_date_string():
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%m/%d/%Y")
    
def get_qdate(date_str):
    from QtCore import QDate
    import datetime
    date = datetime.datetime.strptime(date_str, "%m/%d/%Y")
    return QDate(date.year, date.month, date.day)