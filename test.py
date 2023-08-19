pos = 0
dos = 1

def posi(pos):
    if pos == 0:
        return 1
    elif pos == 1:
        return 0

for i in range(5):
    print("pos before",pos)
    pos = posi(pos)
    print("pos after",pos)
    print("=======")
    print("dos before", dos)
    dos = posi(dos)
    print("dos after", dos)
    print("===========")
