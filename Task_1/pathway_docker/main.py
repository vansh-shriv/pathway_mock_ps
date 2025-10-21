import pathway as pw

table = pw.debug.table_from_markdown("""
    a | b
    1 | 2
    3 | 4
    5 | 6
""")

res = table.reduce(sum_a=pw.reducers.sum(table.a),sum_b=pw.reducers.sum(table.b))
pw.debug.compute_and_print(res)