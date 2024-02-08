import pyhop

'''begin operators'''

def op_punch_for_wood (state, ID):
	if state.time[ID] >= 4:
		state.wood[ID] += 1
		state.time[ID] -= 4
		return state
	return False

def op_craft_wooden_axe_at_bench (state, ID):
	if state.time[ID] >= 1 and state.bench[ID] >= 1 and state.plank[ID] >= 3 and state.stick[ID] >=2:
		state.wooden_axe[ID] += 1
		state.plank[ID] -= 3
		state.stick[ID] -= 2
		state.time[ID] -= 1
		return state
	return False


# added

def op_axe_for_wood(state, ID):
    if state.wooden_axe[ID] > 0 and state.time[ID] >= 2:
        state.wood[ID] += 1 
        state.time[ID] -= 2  # takes 2 time units to collect wood with an axe.
        return state
    return False


def op_convert_wood_to_plank(state, ID):
    if state.wood[ID] > 0:
        state.wood[ID] -= 1 # one log
        state.plank[ID] += 4 # 4 planks
        state.time[ID] -= 1  
        return state
    return False

def op_craft_bench(state, ID):
    if state.plank[ID] >= 4:
        state.plank[ID] -= 4 # 4 planks
        state.bench[ID] = 1  # one bench
        state.time[ID] -= 1 
        return state
    return False

def op_craft_stick(state, ID):
    # Assuming it takes 1 plank to craft 2 sticks.
    if state.plank[ID] >= 2:
        state.plank[ID] -= 2  # 2 planks
        state.stick[ID] += 4  # 4 sticks
        state.time[ID] -= 1 
        return state
    return False


pyhop.declare_operators (op_punch_for_wood, op_craft_wooden_axe_at_bench, op_axe_for_wood, op_convert_wood_to_plank, op_craft_bench, op_craft_stick)

'''end operators'''

def check_enough (state, ID, item, num):
	if getattr(state,item)[ID] >= num: return []
	return False

def produce_enough(state, ID, item, num):
	return [('produce', ID, item), ('have_enough', ID, item, num)]


def produce (state, ID, item):
	if item == 'wood': 
		if state.wooden_axe[ID] > 0:
			return [('op_axe_for_wood', ID)]
		else:   # if axe is not available, try to craft and fallback to punch
			if state.wood[ID] >= 3: # min for bench, sticks, and axe head
				return [('produce_plank', ID), ('produce_sticks', ID), ('produce_wooden_axe', ID)]
			return [('op_punch_for_wood', ID)]

	elif item == 'wooden_axe':
		# this check to make sure we're not making multiple axes
		if state.made_wooden_axe[ID] is True:
			return False
		else:
			state.made_wooden_axe[ID] = True
		return [('produce_wooden_axe', ID)]

	elif item == 'plank':
		return [('op_convert_wood_to_plank', ID)]
	elif item == 'stick':
        # This assumes a method to craft sticks
		return [('op_craft_stick', ID)]
	elif item == 'bench':
        # This assumes a method to craft a bench
		return [('op_craft_bench', ID)]

	else:
		return False

pyhop.declare_methods ('have_enough', check_enough, produce_enough)
pyhop.declare_methods ('produce', produce)

'''begin recipe methods'''

def punch_for_wood (state, ID):
	return [('op_punch_for_wood', ID)]

def craft_wooden_axe_at_bench (state, ID):
	return [('have_enough', ID, 'bench', 1), ('have_enough', ID, 'stick', 2), ('have_enough', ID, 'plank', 3), ('op_craft_wooden_axe_at_bench', ID)]

pyhop.declare_methods ('produce_wood', punch_for_wood)
pyhop.declare_methods ('produce_wooden_axe', craft_wooden_axe_at_bench)


# added

def craft_sticks (state, ID):
	return [('have_enough', ID, 'plank', 2), ('op_craft_stick', ID)]

def craft_plank (state, ID):
	return [('have_enough', ID, 'wood', 1), ('op_convert_wood_to_plank', ID)]

def craft_bench (state, ID):
	return [('have_enough', ID, 'plank', 4), ('op_craft_bench', ID)]


pyhop.declare_methods ('produce_sticks', craft_sticks)
pyhop.declare_methods ('produce_plank', craft_bench)
pyhop.declare_methods ('produce_bench', craft_bench)

'''end recipe methods'''

# declare state
state = pyhop.State('state')
state.wood = {'agent': 0}
#state.time = {'agent': 4}
state.time = {'agent': 46}
state.wooden_axe = {'agent': 0}
state.made_wooden_axe = {'agent': False}

state.plank = {'agent': 0}
state.stick = {'agent': 0}
state.bench = {'agent': 0}

# pyhop.print_operators()
# pyhop.print_methods()

#pyhop.pyhop(state, [('have_enough', 'agent', 'wood', 1)], verbose=3)
pyhop.pyhop(state, [('have_enough', 'agent', 'wood', 12)], verbose=3)