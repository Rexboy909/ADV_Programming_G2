b=[[" "]*3 for _ in range(3)]
p="XO";t=0
while 1:
    for r in b: print(*r)
    i=int(input())-1
    r,c=divmod(i,3)
    if b[r][c]==" ":
        b[r][c]=p[t%2];t+=1
    for i in range(3):
        if b[i][0]==b[i][1]==b[i][2]!=" " or b[0][i]==b[1][i]==b[2][i]!=" ":
            print("win");quit()
    if b[0][0]==b[1][1]==b[2][2]!=" " or b[0][2]==b[1][1]==b[2][0]!=" ":
        print("win");quit()