#Waheed Akram
#The shunting yard Algorithm
#http://www.oxfordmathcenter.com/drupal7/node/628
#Lecturer Ian Mcloughlin

#Defining the function
def shunt(infix):
    #dictionary in phyton, using the 3 operators 
    specials = {'*' : 50 ,'.' :40 ,'|':30}
    stack = ""
    pofix = ""

    #for loop
    for c in infix :
        if c == '(':
            stack = stack + c
        elif c == ')':
            #using while loop
            while stack[-1] != '(':
                #using the code in the same line nd using stack with colons to delete the things from top
                pofix , stack = pofix + stack[-1] , stack[:-1]
                stack = stack[-1]
        elif c in specials:
            #Here c is a charater which is gonna taken from dictionary, o is fuction will start
            #stack will not less than  or equall to -1
            while stack and specials.get(c , 0) <= specials.get(stack[-1],0):
                pofix , stack = pofix + stack[-1] , stack[:-1]
                stack = stack + c
        else:
            pofix = pofix + c 
            while stack:
                pofix , stack = pofix + stack[-1] , stack[:-1]   

    return pofix
    print(shunt("(a.b) | (c*.d)"))