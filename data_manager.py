# Do not modify this file


# read file into a @table
#
# @file_name: string
# @table: list of lists of strings
def get_table_from_file(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()
    table = [element.replace("\n", "").split("\t") for element in lines]
    return table


# write a @table into a file
#
# @file_name: string
# @table: list of lists of strings
def write_table_to_file(file_name, table):
    with open(file_name, "w") as file:
        for record in table:
            for index in range(0, len(record)):
                record[index] = record[index].replace('\r\n', 'LINEBREAK')
            row = '\t'.join(record)
            file.write(row + "\n")
