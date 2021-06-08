count = 0
t = 0
flag = True
while flag:
    for i in [2,40, 65, 81]:
        if i % 2 == 0:
            count += 1
        
        t = t + count

        if t > 10: 
            flag = False 
        
print(t)