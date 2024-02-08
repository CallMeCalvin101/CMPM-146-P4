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

def make_method (name, rule):
	def method (state, ID):
		# your code here
		pass

	return method

def declare_methods (data):
	# some recipes are faster than others for the same product even though they might require extra tools
	# sort the recipes so that faster recipes go first

	# your code here
	# hint: call make_method, then declare the method to pyhop using pyhop.declare_methods('foo', m1, m2, ..., mk)	
	pass			

# Helper Functions
def get_state_value (state, ID, name):
	if (name == "wood"):
		return state.wood[ID]
	elif (name == "time"):
		return state.time[ID]
	elif (name == "cart"):
		return state.cart[ID]
	elif (name == "coal"):
		return state.coal[ID]
	elif (name == "cobble"):
		return state.cobble[ID]
	elif (name == "ingot"):
		return state.ingot[ID]
	elif (name == "ore"):
		return state.ore[ID]
	elif (name == "plank"):
		return state.plank[ID]
	elif (name == "rail"):
		return state.rail[ID]
	elif (name == "stick"):
		return state.stick[ID]
	elif (name == "bench"):
		return state.bench[ID]
	elif (name == "furnace"):
		return state.furnace[ID]
	elif (name == "iron_axe"):
		return state.iron_axe[ID]
	elif (name == "iron_pickaxe"):
		return state.iron_pickaxe[ID]
	elif (name == "stone_axe"):
		return state.stone_axe[ID]
	elif (name == "stone_pickaxe"):
		return state.stone_pickaxe[ID]
	elif (name == "wooden_axe"):
		return state.wooden_axe[ID]
	elif (name == "wooden_pickaxe"):
		return state.wooden_pickaxe[ID]

def modify_state_value (state, ID, name, val):
	if (name == "wood"):
		return state.wood[ID] + val
	elif (name == "time"):
		return state.time[ID] + val
	elif (name == "cart"):
		return state.cart[ID] + val
	elif (name == "coal"):
		return state.coal[ID] + val
	elif (name == "cobble"):
		return state.cobble[ID] + val
	elif (name == "ingot"):
		return state.ingot[ID] + val
	elif (name == "ore"):
		return state.ore[ID] + val
	elif (name == "plank"):
		return state.plank[ID] + val
	elif (name == "rail"):
		return state.rail[ID] + val
	elif (name == "stick"):
		return state.stick[ID] + val
	elif (name == "bench"):
		return state.bench[ID] + val
	elif (name == "furnace"):
		return state.furnace[ID] + val
	elif (name == "iron_axe"):
		return state.iron_axe[ID] + val
	elif (name == "iron_pickaxe"):
		return state.iron_pickaxe[ID] + val
	elif (name == "stone_axe"):
		return state.stone_axe[ID] + val
	elif (name == "stone_pickaxe"):
		return state.stone_pickaxe[ID] + val
	elif (name == "wooden_axe"):
		return state.wooden_axe[ID] + val
	elif (name == "wooden_pickaxe"):
		return state.wooden_pickaxe[ID] + val

def make_operator (rule):
	def operator (state, ID):
		# Checks all possible requirements for the function
		if rule.has_key('Requires'):
			for type, count in rule['Requires']:
				if get_state_value(state, ID, type) < count:
					return False
		if rule.has_key('Consumes'):
			for type, count in rule['Consumes']:
				if get_state_value(state, ID, type) < count:
					return False
		if rule.has_key('Time'):
			if get_state_value(state, ID, 'time') < count:
				return False
		
		if rule.has_key('Produces'):
			if rule.has_key('Consumes'):
				for type, count in rule['Consumes']:
					modify_state_value(state, ID, type, -1 * count)
			
			for type, count in rule['Produces']:
					modify_state_value(state, ID, type, count)
			return state
		return False	
	return operator

def declare_operators (data):
	# Opens and reads Recipes in crafting.json
	data = open('crafting.json')
	data = json.load(data)
	recipes = data['Recipes']

	op_iron_axe_for_wood = make_operator(recipes['iron_axe for wood'])
	op_punch_for_wood = make_operator(recipes['punch for wood'])
	op_craft_wooden_pickaxe_at_bench = make_operator(recipes['craft wooden_pickaxe at bench'])
	op_craft_stone_pickaxe_at_bench = make_operator(recipes['craft stone_pickaxe at bench'])
	op_wooden_pickaxe_for_coal = make_operator(recipes['wooden_pickaxe for coal'])
	op_iron_pickaxe_for_ore = make_operator(recipes['iron_pickaxe for ore'])
	op_wooden_axe_for_wood = make_operator(recipes['wooden_axe for wood'])
	op_craft_plank = make_operator(recipes['craft plank'])
	op_craft_stick = make_operator(recipes['craft stick'])
	op_craft_rail_at_bench = make_operator(recipes['craft rail at bench'])
	op_craft_cart_at_bench = make_operator(recipes['craft cart at bench'])
	op_iron_pickaxe_for_cobble = make_operator(recipes['iron_pickaxe for cobble'])
	op_stone_axe_for_wood = make_operator(recipes['stone_axe for wood'])
	op_craft_iron_pickaxe_at_bench = make_operator(recipes['craft iron_pickaxe at bench'])
	op_craft_furnace_at_bench = make_operator(recipes['craft furnace at bench'])
	op_stone_pickaxe_for_ore = make_operator(recipes['stone_pickaxe for ore'])
	op_craft_iron_axe_at_bench = make_operator(recipes['craft iron_axe at bench'])
	op_stone_pickaxe_for_coal = make_operator(recipes['stone_pickaxe for coal'])
	op_craft_wooden_axe_at_bench = make_operator(recipes['craft wooden_axe at bench'])
	op_stone_pickaxe_for_cobble = make_operator(recipes['stone_pickaxe for cobble'])
	op_wooden_pickaxe_for_cobble = make_operator(recipes['wooden_pickaxe for cobble'])
	op_iron_pickaxe_for_coal = make_operator(recipes['iron_pickaxe for coal'])
	op_craft_bench = make_operator(recipes['craft bench'])
	op_craft_stone_axe_at_bench = make_operator(recipes['craft stone_axe at bench'])
	op_smelt_ore_in_furnace = make_operator(recipes['smelt ore in furnace'])
	pyhop.declare_operators (op_punch_for_wood, op_iron_axe_for_wood, op_craft_wooden_pickaxe_at_bench, op_craft_stone_pickaxe_at_bench, op_wooden_pickaxe_for_coal, 
						  op_iron_pickaxe_for_ore, op_wooden_axe_for_wood, op_craft_plank, op_craft_stick, op_craft_rail_at_bench, op_craft_cart_at_bench, op_iron_pickaxe_for_cobble,
						  op_stone_axe_for_wood, op_craft_iron_pickaxe_at_bench, op_craft_furnace_at_bench, op_stone_pickaxe_for_ore, op_craft_iron_axe_at_bench, op_stone_pickaxe_for_coal,
						  op_craft_wooden_axe_at_bench, op_stone_pickaxe_for_cobble, op_wooden_pickaxe_for_cobble, op_iron_pickaxe_for_coal, op_craft_bench, op_craft_stone_axe_at_bench,
						  op_smelt_ore_in_furnace)

	pass

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

	# pyhop.print_operators()
	# pyhop.print_methods()

	# Hint: verbose output can take a long time even if the solution is correct; 
	# try verbose=1 if it is taking too long
	pyhop.pyhop(state, goals, verbose=3)
	# pyhop.pyhop(state, [('have_enough', 'agent', 'cart', 1),('have_enough', 'agent', 'rail', 20)], verbose=3)
