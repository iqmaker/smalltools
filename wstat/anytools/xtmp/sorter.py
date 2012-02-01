

def sort_list_by_attr( vector, attr ):
    pass

vals = [{'count': 427184, 'base': '', 'value': u'\u0444\u043e\u0440\u0434 \u0444\u043e\u043a\u0443\u0441', 'deep': '', 'label': u'\u0424\u043e\u0440\u0434 \u0444\u043e\u043a\u0443\u0441'}, {'count': 145073, 'base': '', 'value': u'\u043c\u0430\u0437\u0434\u0430 3', 'deep': '', 'label': u'\u041c\u0430\u0437\u0434\u0430 3'}]
print vals
print sorted(vals, key=lambda count: count['count'])