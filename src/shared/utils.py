def get_date_string():
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%m/%d/%Y")
    
def get_qdate(date_str):
    from PyQt5.QtCore import QDate
    if date_str != "":
        import datetime
        date = datetime.datetime.strptime(date_str, "%m/%d/%Y")
        return QDate(date.year, date.month, date.day)
    return QDate(0, 0, 0)
    
def bool_yes_no(value):
    if value:
        return "Yes"
    return "No"
    
def list_add_replace(the_list, obj):
    if obj in the_list:
        idx = the_list.index(obj)
        the_list[idx] = obj
    else:
        the_list.append(obj)