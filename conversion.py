
def conversion_function(integer_list):
    output_string = ""

    for i in range(1, integer_list[0] + 2):
        output_string += chr(integer_list[i] + 97)

    return output_string

# [8, 26, 26, 26, 26, 26, 26, 26, 26]

# [4, 22, 23, 8, 17, 12, 2, 23, 16]
