#tests.py
from Baseline_Design_Package import Fixture_Object,Design_Analysis

def test_Fixture():
	'''
	Tests that only valid fixtures can be created and that internal validations are correct.
	Returns a tuple containing lists of passed tests and failed tests
	'''
	def test_null_TANKO_ID():
		try:
			null_fixt = Fixture_Object.Fixture(None,'CobraHead', 'HPS', 'Intersection', '90degree',None,None, None, None, '70')
			return (False, 'test_null_TANKO_ID()')
		except ValueError:
			return (True, 'test_null_TANKO_ID()')

	def test_validateWattageValue():
		#0: test Null wattage value
		if Fixture_Object.validateWattageValue(None) is not None:
			return (False, 'test_validateWattageValue(): 0') 
		#1: test string wattage value with no integers
		elif Fixture_Object.validateWattageValue('WWW') != 'No wattage - REVIEW':
			return (False, 'test_validateWattageValue(): 1') 
		#2: test string wattage value with integers only
		elif Fixture_Object.validateWattageValue('100') != 100:
			return (False, 'test_validateWattageValue(): 2') 
		#3: test string wattage value with integers and chars
		elif Fixture_Object.validateWattageValue('100W') != 100:
			return (False, 'test_validateWattageValue(): 3') 
		#4: test wattage >400W
		elif Fixture_Object.validateWattageValue('1000') != 1000:
			return (False, 'test_validateWattageValue(): 4') 
		else:
			return (True, 'test_validateWattageValue()')

	def test_DESSTAT():
		prev_des_fixt = Fixture_Object.Fixture(1000,'CobraHead', 'HPS', 'Intersection', '90degree',None, 100, 'Type II', None, '70') 
		nonCH_fixt = Fixture_Object.Fixture(1001,'Decorative', 'HPS', 'Intersection', '90degree',None,None, None, None, '70')
		normal_fixt = Fixture_Object.Fixture(1002,'CobraHead', 'HPS', 'Intersection', '90degree',None,None, None, None, '70')

		if prev_des_fixt.DESSTAT != 'PREVIOUSLY DESIGNED - NO NEW AUTO DESIGN':
			return  (False, 'test_DESSTAT(): Prev Design')
		elif nonCH_fixt.DESSTAT != 'NON-COBRAHEAD - NO AUTO DESIGN':
			return  (False, 'test_DESSTAT(): Non-CH')
		elif normal_fixt.DESSTAT != 'NOT YET DESIGNED':
			return  (False, 'test_DESSTAT(): Normal Fixture')
		else:
			return (True, 'test_DESSTAT()')

	results = [test_null_TANKO_ID(), test_validateWattageValue(), test_DESSTAT() ]
	passed_tests= []
	failed_tests = []

	for result in results:
		if True in result:
			passed_tests.append(result[1])
		elif False in result:
			failed_tests.append(result[1])
		else:
			print('The whole testing process is broken...')
	return (passed_tests,failed_tests)

def test_Design_Analysis():
	'''
	Tests functions in the Design_Analysis module.
	Returns a tuple containing lists of passed tests and failed tests.
	'''
	def test_classifyWattage():
		test_combinations = {
							    'HPS' : {
							  			70 : 'Low', 
							  			150 : 'Medium',
							  			250 : 'High',
							  			400 : 'Very High',
							  			'Review' : 'REVIEW WATTAGE'
							  	},
							    'MV' : {
							   			100 : 'Low',
							   			150 : 'Medium',
							   			400 : 'High',
							   			1000 : 'Very High',
							   			'Review' : 'REVIEW WATTAGE'
						   	    },
						   	    'MH' : {
						   	    		70 : 'Low',
						   	    		150 : 'Medium',
						   	    		200 : 'High',
						   	    		1000 : 'Very High',
						   	    		'Review' : 'REVIEW WATTAGE'
						   	    },
						   	    'INC' : {
						   	    		100 : 'Low',
						   	    		400 : 'REVIEW WATTAGE',
						   	    		'Review' : 'REVIEW WATTAGE'
						   	    },
						   	    'LPS' : {
						   	    		35 : 'Low',
						   	    		70 : 'Medium',
						   	    		150 : 'High',
						   	    		'Review' : 'REVIEW WATTAGE'
						   	    },							  		  
						   	    'Unsure' : { 0 : 'REVIEW LAMP TYPE AND WATTAGE'}
							}
		failed_cases = {}
		number_passed = 0
		for lamp_type,test_case in test_combinations.iteritems():
			for wattage, expected_result in test_case.iteritems():
				case_result = Design_Analysis.classifyWattage(lamp_type, wattage)
				if  case_result != expected_result:
					failed_cases[lamp_type] = (wattage,case_result)
				else:
					number_passed += 1					
		if number_passed == 23:
			return (True, 'test_classifyWattage()')
		else:
			print(number_passed)
			return (False, 'test_classifyWattage() Failed Cases: \n{}'.format([lt + ', '+str(w) for lt,w in failed_cases.iteritems()]))

	def test_classifyDistributionType():
		test_combinations = {
							 'Type IV' : ('Cul-de-sacBulb','90degree','Low'),
							 'Type III' : ('Noneoftheabove', '90degree', 'High'),
							 'Type II' : ('Intersection', '90degree', 'Low'),
							 'Type IV' : ('Intersection', '45degree', 'Medium')
							}
		failed_cases = []
		number_passed = 0
		for expected_result, params in test_combinations.iteritems():
			if Design_Analysis.classifyDistributionType(params[0],params[1],params[2]) != expected_result:
				failed_cases.append({expected_result:params})
			else:
				number_passed += 1
		if number_passed == 3:
			return (True, 'test_classifyDistributionType()')
		else:
			return (False, 'test_classifyDistributionType() failed cases: {}'.format([x for x in failed_cases]))
	results = [test_classifyWattage(),test_classifyDistributionType()]
	passed_tests = []
	failed_tests = []
	for result in results:
		if True in result:
			passed_tests.append(result[1])
		elif False in result:
			failed_tests.append(result[1])
		else:
			print('The whole testing process is broken...')
	return (passed_tests,failed_tests)


Fixture_test_results = test_Fixture()

if len(Fixture_test_results[0]) > 0:
	print('Passed Tests (Fixture): '+'{}'.format([test for test in Fixture_test_results[0]])[1:-1])
else:
	print("Fixture failed all tests.")

if len(Fixture_test_results[1]) > 0:
	print('Failed Tests (Fixture): '+'{}'.format([test for test in Fixture_test_results[1]])[1:-1])
else:
	print("Fixture passed all tests.")

Design_Analysis_test_results = test_Design_Analysis()

if len(Design_Analysis_test_results[0]) > 0:
	print('Passed Tests (Design_Analysis): '+'{}'.format([test for test in Design_Analysis_test_results[0]])[1:-1])
else:
	print("Design_Analysis failed all tests.")

if len(Design_Analysis_test_results[1]) > 0:
	print('Failed Tests (Design_Analysis): '+'{}'.format([test for test in Design_Analysis_test_results[1]])[1:-1])
else:
	print("Design_Analysis passed all tests.")
