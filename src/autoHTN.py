import pyhop
import json

def check_enough (state, ID, item, num):
	if getattr(state,item)[ID] >= num: return []
	return False

def produce_enough (state, ID, item, num):
    return [('produce', ID, item), ('have_enough', ID, item, num)]

pyhop.declare_methods ('have_enough', check_enough, produce_enough)

def produce (state, ID, item):
	return [('produce_{}'.format(item), ID)]

pyhop.declare_methods ('produce', produce)

def make_method(recipe_name, rule):
    def method(state, ID):
        steps = []

        # Check if required tools are available
        for item, amount in rule.get('Requires', {}).items():
            steps.append(('have_enough', ID, item, amount))
            

        # Check if there are enough materials to consume
        for item, amount in rule.get('Consumes', {}).items():
            steps.append(('produce_enough', ID, item, amount))

        # Ensure production of necessary items
        for product, amount in rule.get('Produces', {}).items():
            steps.append(('produce', ID, product))

        return steps
    return method


def declare_methods(data):
    method_map = {}
    for recipe_name, rule in data['Recipes'].items():
        # Generate method for each producible item
        for product in rule.get('Produces', {}).keys():
            if product not in method_map:
                method_map[product] = []
            method_map[product].append(make_method(recipe_name, rule))

    # Declare methods for each product
    for product, methods in method_map.items():
        method_name = 'produce_{}'.format(product.replace("_", " "))
        pyhop.declare_methods(method_name, *methods)
	

def make_operator(rule):
    def operator(state, ID):
   
        for item, amount in rule.get('Requires', {}).items():
            if getattr(state, item)[ID] < amount:
                return False  # Requirement not met

        # Apply "Consumes"
        for item, amount in rule.get('Consumes', {}).items():
            current_amount = getattr(state, item)[ID]
            if current_amount < amount:
                return False  # Not enough resources to consume
            setattr(state, item, {ID: current_amount - amount})

        # Apply "Produces"
        for item, amount in rule.get('Produces', {}).items():
            current_amount = getattr(state, item).get(ID, 0)
            setattr(state, item, {ID: current_amount + amount})

        return state
    return operator


def declare_operators(data):
    for name, rule in data['Recipes'].items():
        pyhop.declare_operators(make_operator(rule))


def add_heuristic (data, ID):
	# prune search branch if heuristic() returns True
	# do not change parameters to heuristic(), but can add more heuristic functions with the same parameters: 
	# e.g. def heuristic2(...); pyhop.add_check(heuristic2)
	def heuristic (state, curr_task, tasks, plan, depth, calling_stack):
		# your code here
		return False # if True, prune this branch

	pyhop.add_check(heuristic)


def set_up_state (data, ID, time=0):
	state = pyhop.State('state')
	state.time = {ID: time}

	for item in data['Items']:
		setattr(state, item, {ID: 0})

	for item in data['Tools']:
		setattr(state, item, {ID: 0})

	for item, num in data['Initial'].items():
		setattr(state, item, {ID: num})

	return state

def set_up_goals (data, ID):
	goals = []
	for item, num in data['Goal'].items():
		goals.append(('have_enough', ID, item, num))

	return goals

if __name__ == '__main__':
	rules_filename = 'crafting.json'

	with open(rules_filename) as f:
		data = json.load(f)

	state = set_up_state(data, 'agent', time=239) # allot time here
	goals = set_up_goals(data, 'agent')

	declare_operators(data) 
	declare_methods(data)
	add_heuristic(data, 'agent')

	pyhop.print_operators()
	pyhop.print_methods()

	# Hint: verbose output can take a long time even if the solution is correct; 
	# try verbose=1 if it is taking too long
	#pyhop.pyhop(state, goals, verbose=3)
	#pyhop.pyhop(state, [('have_enough', 'agent', 'cart', 1),('have_enough', 'agent', 'rail', 20)], verbose=3)
