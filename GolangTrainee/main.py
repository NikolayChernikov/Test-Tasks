#first task
def zero_sort(input_list):
    output_list = sorted(input_list, key=lambda x: not x)
    return output_list

#second task
def row_sum(n: int):
    prev_row: list[int] = []
    n_row: list[int] = []

    if n > 1:
        for i in range(1,n*(n-1),2):
            prev_row.append(i)

        for i in range(prev_row[-1]+2, prev_row[-1]+(n*2)+2, 2):
            n_row.append(i)
    else:
        n_row.append(n)

    return sum(n_row)
    
#fourth task
"""1)12345
   2)call 2  11
     call 1  20
     call 0  21
   3)False"""

#fifth task
def number2letter(n):
   d, m = divmod(n,26)
   return number2letter(d-1)+chr(m+65) if d else chr(m+65)
