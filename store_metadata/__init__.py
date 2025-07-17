import azure.functions as func

def main(metadata: dict, row: func.Out[func.SqlRow]):
    sql_row = func.SqlRow.from_dict(metadata)
    row.set(sql_row)