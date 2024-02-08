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
            steps.append(('have_enough', ID, item, amount))

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
    recipes = data['Recipes']
    def op_iron_axe_for_wood():  
        make_operator(recipes['iron_axe for wood'])
    def op_punch_for_wood(): 
        make_operator(recipes['punch for wood'])
    def op_craft_wooden_pickaxe_at_bench(): 
        make_operator(recipes['craft wooden_pickaxe at bench'])
    def op_craft_stone_pickaxe_at_bench(): 
        make_operator(recipes['craft stone_pickaxe at bench'])
    def op_wooden_pickaxe_for_coal(): 
        make_operator(recipes['wooden_pickaxe for coal'])
    def op_iron_pickaxe_for_ore(): 
        make_operator(recipes['iron_pickaxe for ore'])
    def op_wooden_axe_for_wood(): 
        make_operator(recipes['wooden_axe for wood'])
    def op_craft_plank(): 
        make_operator(recipes['craft plank'])
    def op_craft_stick(): 
        make_operator(recipes['craft stick'])
    def op_craft_rail_at_bench(): 
        make_operator(recipes['craft rail at bench'])
    def op_craft_cart_at_bench(): 
        make_operator(recipes['craft cart at bench'])
    def op_iron_pickaxe_for_cobble(): 
        make_operator(recipes['iron_pickaxe for cobble'])
    def op_stone_axe_for_wood(): 
        make_operator(recipes['stone_axe for wood'])
    def op_craft_iron_pickaxe_at_bench(): 
        make_operator(recipes['craft iron_pickaxe at bench'])
    def op_craft_furnace_at_bench(): 
        make_operator(recipes['craft furnace at bench'])
    def op_stone_pickaxe_for_ore(): 
        make_operator(recipes['stone_pickaxe for ore'])
    def op_craft_iron_axe_at_bench(): 
        make_operator(recipes['craft iron_axe at bench'])
    def op_stone_pickaxe_for_coal(): 
        make_operator(recipes['stone_pickaxe for coal'])
    def op_craft_wooden_axe_at_bench(): 
        make_operator(recipes['craft wooden_axe at bench'])
    def op_stone_pickaxe_for_cobble(): 
        make_operator(recipes['stone_pickaxe for cobble'])
    def op_wooden_pickaxe_for_cobble(): 
        make_operator(recipes['wooden_pickaxe for cobble'])
    def op_iron_pickaxe_for_coal(): 
        make_operator(recipes['iron_pickaxe for coal'])
    def op_craft_bench(): 
        make_operator(recipes['craft bench'])
    def op_craft_stone_axe_at_bench(): 
        make_operator(recipes['craft stone_axe at bench'])
    def op_smelt_ore_in_furnace(): 
        make_operator(recipes['smelt ore in furnace'])
    pyhop.declare_operators(op_punch_for_wood, op_iron_axe_for_wood, op_craft_wooden_pickaxe_at_bench, op_craft_stone_pickaxe_at_bench, op_wooden_pickaxe_for_coal, 
							op_iron_pickaxe_for_ore, op_wooden_axe_for_wood, op_craft_plank, op_craft_stick, op_craft_rail_at_bench, op_craft_cart_at_bench, op_iron_pickaxe_for_cobble,
							op_stone_axe_for_wood, op_craft_iron_pickaxe_at_bench, op_craft_furnace_at_bench, op_stone_pickaxe_for_ore, op_craft_iron_axe_at_bench, op_stone_pickaxe_for_coal,
							op_craft_wooden_axe_at_bench, op_stone_pickaxe_for_cobble, op_wooden_pickaxe_for_cobble, op_iron_pickaxe_for_coal, op_craft_bench, op_craft_stone_axe_at_bench,
							op_smelt_ore_in_furnace)


def add_heuristic (data, ID):
	# prune search branch if heuristic() returns True
	# do not change parameters to heuristic(), but can add more heuristic functions with the same parameters: 
	# e.g. def heuristic2(...); pyhop.add_check(heuristic2)
	def heuristic (state, curr_task, tasks, plan, depth, calling_stack):
		if state.wood[ID] <= 1 and curr_task == 'produce_iron_axe':
			return True
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

	state = set_up_state(data, 'agent', time=250) # allot time here
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
      
	#pyhop.pyhop(state, [('have_enough', 'agent', 'plank', 1)], verbose=3)
