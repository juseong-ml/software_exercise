d = dict()

d['a'] = 1223
d['b'] = 4516

print(d)

ls = []

def base():
    global ls
    ls.append(1)



base()
print(ls)