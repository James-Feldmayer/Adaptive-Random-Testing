
def fut(string):
    for i in range(0, len(string)-1):
        if string[i] == string[i+1]:
            return 1/0

    return string
