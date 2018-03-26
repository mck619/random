def construct_insert_values_string(columns):
    insert_str = '(' +','.join(columns) + ') '
    value_str = ','.join(['%('+column+')s' for column in columns])
    value_str = 'VALUES ({})'.format(value_str)
    return insert_str + value_str