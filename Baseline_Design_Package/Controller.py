import Fixture_Object, Design_Analysis, arcpy
'''
Class: Data Handler
Definition for creating a Data_Handler object that reads/writes data from/to the audit master feature class
'''

class DataHandler(object):
	def __init__(self, feature_class, fields, manufacturer = 'Brand Neutral'):
		self.feature_class = feature_class
		self.fields = fields
		self.manufacturer = manufacturer
		self.fixtures = {}
		print('Data handler initialized.')

	@property
	def feature_class(self):
		return self._feature_class
	@feature_class.setter
	def feature_class(self, value):
		self._feature_class = value

	@property
	def fields(self):
		return self._fields
	@fields.setter
	def fields(self, value):
		self._fields = value

	@property
	def manufacturer(self):
		return self._manufacturer
	@manufacturer.setter
	def manufacturer(self, value):
		approved_manufacturers = ['Brand Neutral']
		if value in approved_manufacturers:
			self._manufacturer = value
		else:
			#to do, loop this back into ui
			raise ValueError('The selected manufacturer is currently not supported.\
			                  Please select a different manufacturer and try again.')

	def apply_design(self):
		print('Applying Design.')
		with arcpy.da.UpdateCursor(self.feature_class,self.fields, '"TANKO_ID" IS NOT NULL') as cursor:
			#loop through all records
			for record in cursor:
				TANKO_ID = record[0]
				FIXTURTYPE = record[1]
				LAMPTYPE = record[2]
				STREETDESN = record[3]
				ARM_DIR = record[4]
				OTHER_WATTAGE = record[5]
				NEW_WATTAGE = record[6]
				DISTRIBUTION_TYPE = record[7]
				DESSTAT = record[8]
				OLD_WATTAGE = record[9]
				fixture = Fixture_Object.Fixture(TANKO_ID, FIXTURTYPE, LAMPTYPE, STREETDESN, ARM_DIR,
		         									  OTHER_WATTAGE, NEW_WATTAGE, DISTRIBUTION_TYPE, DESSTAT,
		         									  OLD_WATTAGE)
				if not fixture.PREVIOUSLY_DESIGNED and 'NON-COBRAHEAD' not in fixture.DESSTAT:
					(fixture.NEW_WATTAGE,fixture.DISTRIBUTION_TYPE,fixture.DESSTAT) = Design_Analysis.recommendDesign(fixture)
					record[6] = fixture.NEW_WATTAGE
					record[7] = fixture.DISTRIBUTION_TYPE
					record[8] = fixture.DESSTAT
				else:
					record[8] = fixture.DESSTAT
				cursor.updateRow(record)
		print('Design written to feature class.')