f = open("Easy.txt", "r")

txt = f.read().split("\n")

for i in txt:
    print(i.replace(" ", ""))