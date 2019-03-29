#Waheed Akram
#G 00341970
#Ian Mcloughlin
#GMIT.ie

#************************************************************
#============= Shunting Yard Algorithm ======================
#*************************************************************
def shunt(infix):

	specials = {'*': 50, '.': 40, '|': 30}

	pofix = ""
	stack = ""

	for c in infix:
		if c == '(':
			stack = stack + c
		elif c == ')':
			while stack[-1] != '(':
				pofix, stack = pofix + stack[-1], stack[:-1]	
			stack = stack[:-1]
		
		elif c in specials:
			while stack and specials.get(c, 0) <= specials.get(stack[-1], 0):
				pofix, stack = pofix + stack[-1], stack[:-1]
			stack = stack + c
		else:
			pofix = pofix + c
					
	while stack:
		pofix, stack = pofix + stack[-1], stack[:-1]

	return pofix
	
#print(shunt("(a.b)|(c*.d)"))


#*******************************************************************
#======================Thomson Constructions========================
#*******************************************************************
class state:
	label = None
	edge1 = None
	edge2 = None
	
class nfa:
	initial = None
	accept = None

	def __init__(self, initial, accept):
		self.initial = initial
		self.accept = accept
	
	def compile(pofix):
		nfastack = []
#for loop	
	for c in pofix:	
#two NFA's of the stack	popping  
		if c == '.':
			nfa2 = nfastack.pop()
			nfa1 =nfastack.pop()
#Connect first NFA's accept state to the second's initial
			nfa1.accept.edge1 = nfa2.initial
# Push NFA to the stack.
			newnfa = nfa(nfa1.initial, nfa2.accept)
			nfastack.append(newnfa)
					
		elif c == '|':
		
# Pop two NFA's off the stack
			nfa2 = nfastack.pop()
			nfa1 = nfastack.pop()
#Create a new initial state, connect it to initial states
# of the two NFA's popped from the stack.
			initial = state()
			initial.edge1 = nfa1.initial
			initial.edge2 = nfa2.initial
#Create new accept state, connecting the accept states
# of the two NFA's popped from the stack, to the new state
			accept = state()
			nfa1.accept.edge1 = accept
			nfa2.accept.edge1 = accept
# Push new NFA to the stack.
			newnfa = nfa(initial, accept)
			nfastack.append(newnfa)
#/////////////////////////////////////////
		elif c == '*':
# Pop a single NFA from the stack.
			nfa1 = nfastack.pop()
# Create new initial and accept state
			initial = state()
			accept = state()
#join the new initial state to nfa1's initial state and the new accept state.
			initial.edge1 = nfa1.initial
			initial.edge2 = accept
#join the old accept state to the new accept state and nfa1's initial state.
			nfa1.accept.edge1 = nfa1.initial
			nfa1.accept.edge2 = accept
# Push new NFA to the stack.
			newnfa = nfa(initial,accept)
			nfastack.append(newnfa)
#/////////////////////////////////////////////
		else:
# Create new initial adn accept states.
			accept = state()
			initial = state()
# Join the initial state the accept state using an arrow labelled c.
			initial.label = c
			initial.edge1 = accept
# Push new NFA to the stack.
			newnfa = nfa(initial, accept)
			nfastack.append(newnfa)
# nfastack should only have a single nfa on it at this point.
	return nfastack.pop()
	

def followes(state):
	states = set()
	states.add(state)
	
	if state.label is None:
		if state.edge1 is not None:
			states |= followes(state.edge1)
		
		if state.edge2 is not None:
			states |= followes(state.edge2)
		
	return states
	
def match(infix, string):
	postfix = shunt(infix)
	nfa = compile(postfix)
	
	current = set()
	next = set()
	
	current |= followes(nfa.initial)
	
	for s in string:
		for c in current:
			if c.label == s:
				next |= followes(c.edge1)
		current = next
		next = set()
	
	return (nfa.accept in current)
		
#=============================================================
infixes = ["a.b.c*", "a.(b|d).c*", "(a.(b|d))*", "a.(b.b)*.c"]
strings = ["", "abc", "abbc", "abcc", "abad", "abbbc"]

for i in infixes:
	for s in strings:
		print(match(i, s), i, s)
	
#print(compile("ab.cd.|"))
#print(compile("aa.*"))


#==============================================================