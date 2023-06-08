
def recurse(val):
    if val < 20:
        return recurse(val + 1)
    else:
        return val
    

print(recurse(0))