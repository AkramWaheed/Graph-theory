#Thompson's Connstruction
#Waheed Akram
#I.D G00341970
#Galway Mayo institute of Technology
#Lecturer Ian Mcloughlin

class state :
	label = None
	edge1 = None
	edge2 = None
	
class nfa  :
	initial = None
	accept  = None
	
def_init_(self,initial,accept):
	self.initial = initial
	self.accept = accept
	
def compile (pofix):
	nfastack = []
	
	for c in pofix:
		if c == '.':
	#pop two NFA's off the stack
		nfa2 = nfastack.pop()
		nfa1 = nfastack.pop()
	#Connnect first NFA accept state to the second's initial
		nfa1.accept.edge1 = nfa.initial
	#push NFA to the stack
		nfastack.append(nfa(nfa1.initial , nfa2.accept))
		
		elif c == '|':
	#pop two NFA's off the stack
		nfa2 = nfastack.pop()
		nfa1 = nfastack.pop()
	#Create new initial state, connect it to initial state of
	#the two NFA's popped from the stack.
		initial = state
		initial.edge1 = nfa1.initial
		initial.edge2 = nfa2.initial
	#Create a new accept state,connecting toaccept states of
	#the two NFA's popped from the srack to the new state
		accept = state()
		nfa1.accept.edge1 = accept
		nfa2.accept.edge1 = accept
	#push new NFA to the stack 
		nfastack.append(nfa(initial , accept))
		
		elif c == '*':
	#pop signle NFA from the stack
		nfa1 = nfastack.pop()
	#Create new initial & accept states 
		initial = state()
		accept = state()
	#Join the new state to NFA's initial state & the new accept state
		initial.edge1 = nfa1.initial
		initial.edge2 = accept
	#Join the old accept state to the new state & NFA's initial state
		nfa1.accept.edge1 = nfa1.initial
		nfa1.accept.edge2 = accept
	#Push new Nfa to the new stack
		nfastack.append(nfa(initial , accept))
		
		else :
	#Create new initial & accept state
		accept = state()
		initial = state()
	#join the initial state & accept using an arrow labelled c 
		initial.label = c
		initial.edge1 = accept
	#Push new NFA to the stack
		nfastack.append(nfa(initial , accept))
	#NFA stack onlyhave single NFA on it at this point	
		return nfastack.pop()
		
	print(compile("ab.cd.|"))
		
