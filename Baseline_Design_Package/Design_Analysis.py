'''
Design_Analysis.py
Functions to classify wattage and distribution type 
'''
def classifyWattage(lamp_type, old_wattage):
	'''
	Returns a wattage classification to a fixture based on existing wattage
	and lamp type
	'''
	#High Pressure Sodium
	try:
		old_wattage = int(old_wattage)
	except ValueError:
		return 'REVIEW WATTAGE'

	if lamp_type == 'HPS':
		if old_wattage <= 70:
			return 'Low'
		elif 70 < old_wattage <= 175:
			return 'Medium'
		elif 175 < old_wattage <= 250:
			return 'High'
		elif old_wattage > 250:
			return 'Very High'
		else:
			return 'REVIEW WATTAGE'
	#Mercury Vapor
	elif lamp_type == 'MV':
		if old_wattage <= 100:
			return 'Low'
		elif 100 < old_wattage <= 250:
			return 'Medium'
		elif 250 < old_wattage <= 400:
			return 'High'
		elif old_wattage > 400:
			return 'Very High'
		else:
			return 'REVIEW WATTAGE'
	#Metal Halide
	elif lamp_type == 'MH':
		if old_wattage <= 70:
			return 'Low'
		elif 70 < old_wattage <= 175:
			return 'Medium'
		elif 175 < old_wattage <= 400:
			return 'High'
		elif old_wattage > 400:
			return 'Very High'
		else:
			return 'REVIEW WATTAGE'
	#Incandescent
	elif lamp_type == 'INC':
		if old_wattage <= 200:
			return 'Low'
		else:
			return 'REVIEW WATTAGE'
	#Low Pressure Sodium
	elif lamp_type == 'LPS':
		if old_wattage <= 35:
			return 'Low'
		elif 35 < old_wattage <= 90:
			return 'Medium'
		elif 90 < old_wattage <= 180:
			return 'High'
		else:
			return 'REVIEW WATTAGE'
	elif lamp_type == 'LED':
		return 'EXISTING LED'
	#Induction/Unsure/Invalid Lamp Type
	else:
		return 'REVIEW LAMP TYPE AND WATTAGE'

def classifyDistributionType(street_design,arm_direction,design_wattage):
	'''
	Returns a Distribution Type based on street design, arm dir, and wattage classification fields
	'''
	if street_design in ['Cul-de-sacBulb','Knuckle'] or (arm_direction == '45degree' and 'Intersection' in street_design):
		return 'Type IV'
	elif arm_direction in ['Parallel', 'FixtureDoesNotLightStreet', 'Other']:
		return 'REVIEW ARM DIRECTION'
	else:
		if design_wattage in ['High', 'Very High']:
			return 'Type III'
		else:
			return 'Type II'

def recommendDesign(fixture):
	'''
	Recommends a wattage and distribution type.
	Returns a tuple:
	(Recommended Wattage, Recommended Distribution Type, 'AUTO DESIGN')

	'''
	recommended_wattage = classifyWattage(fixture.LAMPTYPE, fixture.OLD_WATTAGE)
	recommended_distribution_type = classifyDistributionType(fixture.STREETDESN,fixture.ARM_DIR,recommended_wattage)
	return (recommended_wattage,recommended_distribution_type,'AUTO_DESIGN')
