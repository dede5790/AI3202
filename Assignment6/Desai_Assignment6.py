#Deep Desai
#CSCI 3202
#Assignment6
import getopt, sys
#Discussed strategy with Mitch Zinser, Brady Auen and Chris Meyer
#resources used http://www.tutorialspoint.com/python/python_dictionary.htm, and http://homes.soic.indiana.edu/classes/spring2012/csci/b553-hauserk/bayesnet.py
#Node class that stores its parents, its conditional probability
class BayesNode:
	def __init__(self):
		self.parents = []
		self.conditionals = {}
	#Takes in a list of parents to the node, adds them to the parent list
	def set_parents(self, parent_list):
		for i in parent_list:
			self.parents.append(i)
	#Takes in the condition and probability and adds them to the conditional probability table for the node
	def set_conditional(self, condition, prob):
		self.conditionals[condition] = prob
	#Returns a list of the nodes parents
	def get_parents(self):
		return self.parents
	#Returns the conditional dict
	def get_conditional(self):
		return self.conditionals
#Function to calculate the MargProbability probabillity of the passed in node
def MargProbability(graph, args):
	#Check for Tilda (reverses true/false)
	if args[0] == "~":
		#Call MargProbability on the letter
		marg = MargProbability(graph, args[1])
		return ("Not " + marg[0], 1-marg[1])
	#Else the cmd line arg is a single letter
	#Pollution
	elif args.upper() == "P":
		return ("Pollution", graph["Pollution"].get_conditional()["p"])
	#Smoker
	elif args.upper() == "S":
		return ("Smoker", graph["Smoker"].get_conditional()["s"])
	#Cancer
	elif args.upper() == "C":
		#Get conditional dict from cancer node
		CondDictionary = graph["Cancer"].get_conditional()
		#Get MargProbability probabilities for pollution and smoker
		polMarginal = graph["Pollution"].get_conditional()["p"]
		smokerMarginal = graph["Smoker"].get_conditional()["s"]
		#Calculate part of tree that assumes p
		p = (CondDictionary["ps"]*smokerMarginal) + (CondDictionary["p~s"]*(1-smokerMarginal))
		#Calculate part of tree that assumes ~p
		not_p = (CondDictionary["~ps"]*smokerMarginal)+ (CondDictionary["~p~s"]*(1-smokerMarginal))
		#Add parts of tree together and multiply by prob of p or ~p
		marg = (polMarginal*p) + ((1-polMarginal)*not_p)
		return ("Cancer", marg)
	#XRay
	elif args.upper() == "X":
		#Get conditional dict ffor xray node
		CondDictionary = graph["XRay"].get_conditional()
		#Calculate MargProbability probability for cancer
		cancerMarginal = MargProbability(graph, "C")[1]
		#Calculate MargProbability of XRay using conditional table and MargProbability prob
		marg = (CondDictionary["c"]*cancerMarginal) + (CondDictionary["~c"]*(1-cancerMarginal))
		return ("XRay", marg)
	#Dyspnoea
	elif args.upper() == "D":
		#Get conditional dict ffor xray node
		CondDictionary = graph["Dyspnoea"].get_conditional()
		#Calculate MargProbability probability for cancer
		cancerMarginal = MargProbability(graph, "C")[1]
		#Calculate MargProbability of XRay using conditional table and MargProbability prob
		marg = (CondDictionary["c"]*cancerMarginal) + (CondDictionary["~c"]*(1-cancerMarginal))
		return ("Dyspnoea", marg)
#Function to calculate the conditional probability of the first arg (before) given the second arg(s) (after)
def conditional(graph, before, after):
	Tilda = False
	#Check for Tilda
	if before[0] == "~":
		Tilda = True
		before = before[1]
	#Check if the before is in the after
	if before in after:
		return 1
	#Get conditional dictionaries for each node
	polConditional = graph["Pollution"].get_conditional()
	smokeConditional = graph["Smoker"].get_conditional()
	CancerConditional = graph["Cancer"].get_conditional()
	xrayConditional = graph["XRay"].get_conditional()
	dysConditional = graph["Dyspnoea"].get_conditional()
	#Check for the before condition
	#Pollution
	if before.upper() == "P":
		#Check if the probability is already calculated
		if after in polConditional:
			return polConditional[after]
		#Otherwise start case matching
		elif Tilda:
			#If ~p|d
			if after == "d":
				return (conditional(graph,"d","~p")*polConditional["~p"])/MargProbability(graph,"D")[1]
			#If ~p|c
			elif after == "c":
				return (conditional(graph,"c","~p")*polConditional["~p"])/MargProbability(graph,"c")[1]
			#~p|cs
			elif (after == "cs") or (after == "sc"):
				#Numerator
				numerator = CancerConditional["~ps"]*smokeConditional["s"]*polConditional["~p"]
				#Denominator
				denominator = CancerConditional["~ps"]*smokeConditional["s"]*polConditional["~p"]+CancerConditional["ps"]*smokeConditional["s"]*polConditional["p"]
				return numerator/denominator
			#~p|ds
			elif (after == "ds") or (after == "sd"):
				#Store Numerator and Denominator
				numerator = []
				denominator = []
				#Calculate numerators
				numerator.append(dysConditional["c"]*CancerConditional["~ps"]*polConditional["~p"]*smokeConditional["s"])
				numerator.append(dysConditional["~c"]*(1-CancerConditional["~ps"])*polConditional["~p"]*smokeConditional["s"])
				denominator.append(dysConditional["c"]*CancerConditional["~ps"]*polConditional["~p"]*smokeConditional["s"])
				denominator.append(dysConditional["c"]*CancerConditional["ps"]*polConditional["p"]*smokeConditional["s"])
				denominator.append(dysConditional["~c"]*(1-CancerConditional["~ps"])*polConditional["~p"]*smokeConditional["s"])
				denominator.append(dysConditional["~c"]*(1-CancerConditional["ps"])*polConditional["p"]*smokeConditional["s"])
				#Calculate denominators
				return sum(numerator)/sum(denominator)
			#~p|s Independant, just MargProbability of p ~p
			elif after == "s":
				return MargProbability(graph,"~p")[1]
	#Smoking
	elif before.upper() == "S":
		#Check if the probability is already calculated
		if after in smokeConditional:
			return smokeConditional[after]
		#Otherwise start case matching
		elif not Tilda:
			#s|c
			if after == "c":
				return (conditional(graph,"c","s")*smokeConditional["s"])/MargProbability(graph,"c")[1]
			#s|d
			elif after == "d":
				return (conditional(graph,"d","s")*smokeConditional["s"])/MargProbability(graph,"d")[1]
	#Cancer
	elif before.upper() == "C":
		#Check if the probability is already calculated
		if after in CancerConditional:
			return CancerConditional[after]
		#Otherwise start case matching
		elif not Tilda:
			#c|s
			if after == "s":
				return ((CancerConditional["ps"]*polConditional["p"]*smokeConditional["s"])+(CancerConditional["~ps"]*polConditional["~p"]*smokeConditional["s"]))/smokeConditional["s"]
			#c|ds
			elif (after == "ds") or (after =="sd"):
				#Store Numerator and Denomerator
				numerator = []
				denominator = []
				#Calculate numerators
				numerator.append(dysConditional["c"]*CancerConditional["ps"]*polConditional["p"]*smokeConditional["s"])
				numerator.append(dysConditional["c"]*CancerConditional["~ps"]*polConditional["~p"]*smokeConditional["s"])
				#Calculate denominators
				denominator.append(dysConditional["c"]*CancerConditional["ps"]*polConditional["p"]*smokeConditional["s"])
				denominator.append(dysConditional["c"]*CancerConditional["~ps"]*polConditional["~p"]*smokeConditional["s"])
				denominator.append(dysConditional["~c"]*(1-CancerConditional["ps"])*polConditional["p"]*smokeConditional["s"])
				denominator.append(dysConditional["~c"]*(1-CancerConditional["~ps"])*polConditional["~p"]*smokeConditional["s"])
				return sum(numerator)/sum(denominator)
			#c|d
			elif after == "d":
				return (dysConditional["c"]*MargProbability(graph,"c")[1])/MargProbability(graph,"d")[1]
			#c|~p
			elif after == "~p":
				#Store Numerator
				numerator = []
				#Calculate numerator
				numerator.append(CancerConditional["~ps"]*polConditional["~p"]*smokeConditional["s"])
				numerator.append(CancerConditional["~p~s"]*polConditional["~p"]*smokeConditional["~s"])
				return sum(numerator)/polConditional["~p"]
			#c|p
			elif after == "p":
				#Store Numerator
				numerator = []
				#Calculate numerator
				numerator.append(CancerConditional["ps"]*polConditional["p"]*smokeConditional["s"])
				numerator.append(CancerConditional["p~s"]*polConditional["p"]*smokeConditional["~s"])
				return sum(numerator)/polConditional["p"]
	#XRay
	elif before.upper() == "X":
		#Check if the probability is already calculated
		if after in xrayConditional:
			return xrayConditional[after]
		#Otherwise start case matching
		elif not Tilda:
			#x|s
			if after == "s":
				#Store Numerator and Denomerator
				numerator = []
				denominator = []
				#Calculate numerators
				numerator.append(xrayConditional["c"]*(CancerConditional["ps"]*smokeConditional["s"]*polConditional["p"]))
				numerator.append(xrayConditional["c"]*(CancerConditional["~ps"]*smokeConditional["s"]*polConditional["~p"]))
				numerator.append(xrayConditional["~c"]*((1-CancerConditional["ps"])*smokeConditional["s"]*polConditional["p"]))
				numerator.append(xrayConditional["~c"]*((1-CancerConditional["~ps"])*smokeConditional["s"]*polConditional["~p"]))
				#Calculate denominators
				denominator.append(CancerConditional["ps"]*polConditional["p"]*smokeConditional["s"])
				denominator.append(CancerConditional["~ps"]*polConditional["~p"]*smokeConditional["s"])
				denominator.append((1-CancerConditional["ps"])*polConditional["p"]*smokeConditional["s"])
				denominator.append((1-CancerConditional["~ps"])*polConditional["~p"]*smokeConditional["s"])
				return sum(numerator)/sum(denominator)
			#x|d
			elif after == "d":
				return (((xrayConditional["c"]*MargProbability(graph,"c")[1]*dysConditional["c"])+(xrayConditional["~c"]*MargProbability(graph,"~c")[1]*dysConditional["~c"]))/MargProbability(graph,"d")[1])
			#x|ds
			elif (after == "ds") or (after == "sd"):
				#Store Numerator and Denomerator
				numerator = []
				denominator = []
				#Calculate numerators
				numerator.append(xrayConditional["c"]*dysConditional["c"]*CancerConditional["~ps"]*polConditional["~p"]*smokeConditional["s"])
				numerator.append(xrayConditional["~c"]*dysConditional["~c"]*(1-CancerConditional["~ps"])*polConditional["~p"]*smokeConditional["s"])
				numerator.append(xrayConditional["c"]*dysConditional["c"]*CancerConditional["ps"]*polConditional["p"]*smokeConditional["s"])
				numerator.append(xrayConditional["~c"]*dysConditional["~c"]*(1-CancerConditional["ps"])*polConditional["p"]*smokeConditional["s"])
				#Calculate denominators
				denominator.append(dysConditional["c"]*CancerConditional["~ps"]*polConditional["~p"]*smokeConditional["s"])
				denominator.append(dysConditional["~c"]*(1-CancerConditional["~ps"])*polConditional["~p"]*smokeConditional["s"])
				denominator.append(dysConditional["c"]*CancerConditional["ps"]*polConditional["p"]*smokeConditional["s"])
				denominator.append(dysConditional["~c"]*(1-CancerConditional["ps"])*polConditional["p"]*smokeConditional["s"])
				return sum(numerator)/sum(denominator)
			#x|cs
			elif (after == "cs") or (after == "sc"):
				return conditional(graph,"x","c")
	#Dyspnoea
	elif before.upper() == "D":
		#Check if the probability is already calculated
		if after in dysConditional:
			return dysConditional[after]
		#Otherwise start case matching
		elif not Tilda:
			#d|~p
			if after == "~p":
				#Store Numerator and Denomerator
				numerator = []
				denominator = []
				#Calculate numerators
				numerator.append(dysConditional["c"]*(CancerConditional["~ps"]*smokeConditional["s"]*polConditional["~p"]))
				numerator.append(dysConditional["c"]*(CancerConditional["~p~s"]*smokeConditional["~s"]*polConditional["~p"]))
				numerator.append(dysConditional["~c"]*((1-CancerConditional["~ps"])*smokeConditional["s"]*polConditional["~p"]))
				numerator.append(dysConditional["~c"]*((1-CancerConditional["~p~s"])*smokeConditional["~s"]*polConditional["~p"]))
				#Calculate denominators
				denominator.append(CancerConditional["~ps"]*polConditional["~p"]*smokeConditional["s"])
				denominator.append(CancerConditional["~p~s"]*polConditional["~p"]*smokeConditional["~s"])
				denominator.append((1-CancerConditional["~ps"])*polConditional["~p"]*smokeConditional["s"])
				denominator.append((1-CancerConditional["~p~s"])*polConditional["~p"]*smokeConditional["~s"])
				return sum(numerator)/sum(denominator)
			#d|s
			elif after == "s":
				#Store Numerator and Denomerator
				numerator = []
				denominator = []
				#Calculate numerators
				numerator.append(dysConditional["c"]*(CancerConditional["ps"]*smokeConditional["s"]*polConditional["p"]))
				numerator.append(dysConditional["c"]*(CancerConditional["~ps"]*smokeConditional["s"]*polConditional["~p"]))
				numerator.append(dysConditional["~c"]*((1-CancerConditional["ps"])*smokeConditional["s"]*polConditional["p"]))
				numerator.append(dysConditional["~c"]*((1-CancerConditional["~ps"])*smokeConditional["s"]*polConditional["~p"]))
				#Calculate denominators
				denominator.append(CancerConditional["ps"]*polConditional["p"]*smokeConditional["s"])
				denominator.append(CancerConditional["~ps"]*polConditional["~p"]*smokeConditional["s"])
				denominator.append((1-CancerConditional["ps"])*polConditional["p"]*smokeConditional["s"])
				denominator.append((1-CancerConditional["~ps"])*polConditional["~p"]*smokeConditional["s"])
				return sum(numerator)/sum(denominator)
			#d|c
			elif after == "c":
				return (conditional(graph,"c","d")*MargProbability(graph,"d")[1])/MargProbability(graph)[1]
			#x|cs
			elif (after == "cs") or (after == "sc"):
				return conditional(graph,"d","c")
				
#Function to calculate the joint probability
def joint(graph,a):
	args = parse_string(a)
	if len(args) == 2:
		return conditional(graph,args[0],args[1]) * MargProbability(graph,a[1])[1]
	else:
		return conditional(graph,a[0],a[1]) * joint(a[1],a[2:])
#Helper functino to return a list of variables from a string
def parse_string(args):
	#Store if the last character was a ~
	skip = False
	#List to store the individual args
	arg_list = []
	#Iterate through the characters of the args string
	for i in args:
		#If the last char was ~, reset skip and add ~ + current char to args list
		if skip:
			skip = False
			arg_list.append("~"+i)
		#Otherwise, last char was not ~
		else:
			#If current char is ~, set skip to true for next loop
			if i == "~":
				skip = True
			#Otherwise add char to arg list
			else:
				arg_list.append(i)
	return arg_list
#Takes in string of args, returns list of all possible combos for args
def joint_more(args):
	joint_more = []
	#Remove ~ from args
	args = args.replace("~","")
	joint_more.append(args[0])
	joint_more.append("~" + args[0])
	#Iterate through joint var list (Add first arg and ~first arg to joint var list)
	for i in range(1, len(args)):
		temp_list = []
		for var in joint_more:
			temp_list.append(var + args[i])
			temp_list.append(var + "~" + args[i])
		joint_more = temp_list
	return joint_more

#Only run this if file is beng run directly
if __name__ == "__main__":
	'''Create the Bayes Net and insert probability tables'''
	#Dictionary to store nodes
	BayesNet = {}
	#Create nodes
	BayesNet["Pollution"] = BayesNode()
	BayesNet["Smoker"] = BayesNode()
	BayesNet["Cancer"] = BayesNode()
	BayesNet["XRay"] = BayesNode()
	BayesNet["Dyspnoea"] = BayesNode()
	#Set parents for nodes
	BayesNet["Cancer"].set_parents([BayesNet["Pollution"],BayesNet["Smoker"]])
	BayesNet["XRay"].set_parents([BayesNet["Cancer"]])
	BayesNet["Dyspnoea"].set_parents([BayesNet["Cancer"]])
	#Set conditional probabilities for each node
	#Pollution
	BayesNet["Pollution"].set_conditional("p",0.9) #Low pol
	BayesNet["Pollution"].set_conditional("~p",0.1) #High pol
	#Smoker
	BayesNet["Smoker"].set_conditional("s",0.3) #Smoker
	BayesNet["Smoker"].set_conditional("~s",0.7) #Not smoker
	#Cancer
	BayesNet["Cancer"].set_conditional("~ps",0.05) #High pol, smoker
	BayesNet["Cancer"].set_conditional("~p~s",0.02) #High pol, not smoker
	BayesNet["Cancer"].set_conditional("ps",0.03) #Low pol, smoker
	BayesNet["Cancer"].set_conditional("p~s",0.001) #Low pol, not smoker
	#Account for the input being backwards
	BayesNet["Cancer"].set_conditional("s~p",0.05) #High pol, smoker
	BayesNet["Cancer"].set_conditional("~s~p",0.02) #High pol, not smoker
	BayesNet["Cancer"].set_conditional("sp",0.03) #Low pol, smoker
	BayesNet["Cancer"].set_conditional("~sp",0.001) #Low pol, not smoker
	#XRay
	BayesNet["XRay"].set_conditional("c",0.9) #Cancer
	BayesNet["XRay"].set_conditional("~c",0.2) #Not cancer
	#Dyspnoea
	BayesNet["Dyspnoea"].set_conditional("c",0.65) #Cancer
	BayesNet["Dyspnoea"].set_conditional("~c",0.3)
	'''Parse for input and start calculations'''
	try:
		opts, args = getopt.getopt(sys.argv[1:], "m:g:j:p:")
	except getopt.GetoptError as err:
		# print help information and exit:
		print(str(err)) # will printsomething like "option -a not recognized"
		sys.exit(2)
	for o, a in opts:
		if o in ("-p"):
			print("flag", o)
			print("args", a)
			#print(a[0]) #Variable to change prior
			#print(float(a[1:])) #Value to change prior to
			#Check which variable to change prior
			#If pollution
			if a[0] == "P":
				#Change prior
				BayesNet["Pollution"].set_conditional("p",float(a[1:]))
				BayesNet["Pollution"].set_conditional("~p",1-float(a[1:]))
			#If Smoker
			elif a[0] == "S":
				#Change prior
				BayesNet["Smoker"].set_conditional("s",float(a[1:]))
				BayesNet["Smoker"].set_conditional("~s",1-float(a[1:]))
		elif o in ("-m"):
			#print("flag", o)
			#print("args", a)
			#print(type(a))
			marg = MargProbability(BayesNet, a)
			print("MargProbability of", marg[0], "=", marg[1])
		elif o in ("-g"): #TODO
			#print("flag", o)
			#print("args", a)
			#print(type(a))
			'''you may want to parse a here and pass the left of |
			and right of l as arguments to conditional
			'''
			p = a.find("l")
			print(a[:p],"given",a[p+1:])
			#print(a[p+1:])
			cond = conditional(BayesNet,a[:p],a[p+1:])
			print(cond)
		elif o in ("-j"):
			#print("flag", o)
			#print("args", a)
			print("Joint probability for",a)
			if len(a) < 2:
				print(MargProbability(BayesNet,a))
			else:
				print(joint(BayesNet,a))
			
			#calcJointDistribution(BayesNet,a)
		else:
			assert False, "unhandled option"
