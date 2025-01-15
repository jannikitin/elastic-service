try:
    10 / 0
except ZeroDivisionError as e:
    print(e.__repr__())
    print(e.args)
    # print(e.__annotations__)
