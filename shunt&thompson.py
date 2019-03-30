#Regular Expression Matcher
#Waheed Akram
#ID G00341970
#GMIT Ireland
def shunt(infix):
#The Shunting yard Algorithm for converting infix regular expression to postfix.
    #Spcial characters for regular expression and this precedence
	specials = {'*': 50, '.': 40, '|': 30}
	#Will eventually be the ouptput
	pofix = ""
	#operator stack	
	stack = ""
	#Loop through the string a character st a time
	for c in infix:
	#If an open bracket , push to the stack
		if c == '(':
			stack = stack + c
	#if closing bracket,pop from stack ,push to output until open bracket		
		elif c == ')':
			while stack[-1] != '(':
				pofix, stack = pofix + stack[-1], stack[:-1]	
			stack = stack[:-1]
	#if it's an operator,push to stack after popping lower or equal precedence
	#Operators from top of stack into output
		elif c in specials:
			while stack and specials.get(c, 0) <= specials.get(stack[-1], 0):
				pofix, stack = pofix + stack[-1], stack[:-1]
			stack = stack + c
	#Regular character are pushed immideiately to the output		
		else:
			pofix = pofix + c
	#pop all remaining operators from stack to output 				
	while stack:
		pofix, stack = pofix + stack[-1], stack[:-1]
	#Return postfix regex
	return pofix
	
	
	#Represent a stack with two arrows, labelled by label
	#Use none for label represnting "e" arrows
class state:
	label = None
	edge1 = None
	edge2 = None
	#An NFA is represented by its initial and accept states
class nfa:
	initial = None
	accept = None

	def __init__(self, initial, accept):
		self.initial = initial
		self.accept = accept
	
def compile(pofix):
#""" Compile is a pofix regular expression into NFA """
	nfastack = []
	
	for c in pofix:	
		
		if c == '.':
	#Pop Two NFA's off the stack	
			nfa2 = nfastack.pop()
			nfa1 =nfastack.pop()
	#Connect first NFA's accept state to the second's intial			
			nfa1.accept.edge1 = nfa2.initial
	#Push NFA to the stack			
			newnfa = nfa(nfa1.initial, nfa2.accept)
			nfastack.append(newnfa)
			
				
		elif c == '|':
	#pop two NFA off the stack 	
			nfa2 = nfastack.pop()
			nfa1 = nfastack.pop()
	#Create a new initial atate , connnect it to initial state of the two NFA's popped from the stack to the new stack	
			initial = state()
			initial.edge1 = nfa1.initial
			initial.edge2 = nfa2.initial
	#Create a new accept atate , connnecting the accept state of the two NFA's popped from the stack to the new stack		
			accept = state()
			nfa1.accept.edge1 = accept
			nfa2.accept.edge1 = accept
	#Push new NFA to the stack 		
			newnfa = nfa(initial, accept)
			nfastack.append(newnfa)
				
		elif c == '*':
	#Pop a signle NFA from the stack 
			nfa1 = nfastack.pop()
	#Create new initial & accept state states 	
			initial = state()
			accept = state()
	#Join the new initial state to the new accept state and nfa's intial state 
			initial.edge1 = nfa1.initial
			initial.edge2 = accept
	#Push new NFA to the stack		
			nfa1.accept.edge1 = nfa1.initial
			nfa1.accept.edge2 = accept
			
			newnfa = nfa(initial,accept)
			nfastack.append(newnfa)
		
		
		else:
	#Create new intial & accept states			
			accept = state()
			initial = state()
	#Join the initial state the accept state using an arrow labelled c			
			initial.label = c
			initial.edge1 = accept
	#puah new NFA to the stack			
			newnfa = nfa(initial, accept)		
			nfastack.append(newnfa)
	#nfastack should only have a single nfa on it at this point 			
	return nfastack.pop()
	

def followes(state):
#""" Return the set of states that can be reached from state following a arrows """
#Create a new set , with states as its only member 
	states = set()
	states.add(state)
#Check if state has arrows labelled a from it 	
	if state.label is None:
#if there is an edge1 , follow it	
		if state.edge1 is not None:
			states |= followes(state.edge1)
#if there is an edge2 , follow it		
		if state.edge2 is not None:
			states |= followes(state.edge2)
#Return the set of states 		
	return states
	
def match(infix, string):
#""" Matches string to infix regular expression """
#Shunt & compile the reular expression
	postfix = shunt(infix)
	nfa = compile(postfix)
#The current set of states and the next of states	
	current = set()
	next = set()
#Add the initial state to the current set.	
	current |= followes(nfa.initial)
#Loop through each character in the string	
	for s in string:
#Loop through the current set of the state 
		for c in current:
#check if that state is labelled s 		
			if c.label == s:
#Add the edge1 state to the next set 			
				next |= followes(c.edge1)
#Set Current to next , and clear out next
		current = next
		next = set()
#Check if the accept state is in the set of current states	
	return (nfa.accept in current)
		

infixes = ["a.b.c*", "a.(b|d).c*", "(a.(b|d))*", "a.(b.b)*.c","a+b+c*d"]
strings = ["", "abc", "abbc", "abcc", "abad", "abbbc","abcd"]

for i in infixes:
	for s in strings:
		print(match(i, s), i, s)
	



