import re
'''
Class: Fixture
Definition for creating a Fixture object that can be passed around and used for analysis
'''
class Fixture(object):
	def __init__(self, TANKO_ID, FIXTURTYPE, LAMPTYPE, STREETDESN, ARM_DIR,
		         OTHER_WATTAGE, NEW_WATTAGE, DISTRIBUTION_TYPE, DESSTAT,
		         OLD_WATTAGE):
		self.TANKO_ID = TANKO_ID
		self.FIXTURTYPE = FIXTURTYPE
		self.LAMPTYPE = LAMPTYPE
		self.STREETDESN = STREETDESN
		self.ARM_DIR = ARM_DIR
		self.OTHER_WATTAGE = OTHER_WATTAGE
		self.NEW_WATTAGE = NEW_WATTAGE
		self.DISTRIBUTION_TYPE = DISTRIBUTION_TYPE
		self.OLD_WATTAGE = OLD_WATTAGE
		if self.NEW_WATTAGE is not None or self.DISTRIBUTION_TYPE is not None:
			self.PREVIOUSLY_DESIGNED = True
		else:
			self.PREVIOUSLY_DESIGNED = False
		self.DESSTAT = DESSTAT
	@property
	def TANKO_ID(self):
		return self._TANKO_ID
	@TANKO_ID.setter
	def TANKO_ID(self,value):
		if value is not None:
			self._TANKO_ID = value
		else:
			raise ValueError('Fixture does not have a Tanko ID')
	
	@property
	def FIXTURTYPE(self):
		return self._FIXTURTYPE
	@FIXTURTYPE.setter
	def FIXTURTYPE(self,value):
		self._FIXTURTYPE = value

	@property
	def LAMPTYPE(self):
		return self._LAMPTYPE
	@LAMPTYPE.setter
	def LAMPTYPE(self,value):
		self._LAMPTYPE = value
	
	@property
	def STREETDESN(self):
		return self._STREETDESN
	@STREETDESN.setter
	def STREETDESN(self,value):
		self._STREETDESN = value
	
	@property
	def ARM_DIR(self):
		return self._ARM_DIR
	@ARM_DIR.setter
	def ARM_DIR(self,value):
		self._ARM_DIR = value

	@property
	def OTHER_WATTAGE(self):
		return self._OTHER_WATTTAGE
	@OTHER_WATTAGE.setter
	def OTHER_WATTAGE(self,value):
		self._OTHER_WATTTAGE = validateWattageValue(value)
	
	@property
	def NEW_WATTAGE(self):
		return self._NEW_WATTAGE
	@NEW_WATTAGE.setter
	def NEW_WATTAGE(self,value):
		self._NEW_WATTAGE = value
	
	@property
	def DISTRIBUTION_TYPE(self):
		return self._DISTRIBUTION_TYPE
	@DISTRIBUTION_TYPE.setter
	def DISTRIBUTION_TYPE(self,value):
		self._DISTRIBUTION_TYPE = value
	
	@property
	def DESSTAT(self):
		return self._DESSTAT
	@DESSTAT.setter
	def DESSTAT(self, value):
		if self.PREVIOUSLY_DESIGNED:
			if value is None:
				self._DESSTAT = 'PREVIOUSLY DESIGNED - NO NEW AUTO DESIGN'
			else:
				new_status = 'PREVIOUSLY DESIGNED - NO NEW AUTO DESIGN; {}'.format(value)
				self._DESSTAT = new_status[0:100]
		elif self.FIXTURTYPE != 'CobraHead':
			self._DESSTAT = 'NON-COBRAHEAD - NO AUTO DESIGN'
		elif value is not None:
			self._DESSTAT = value
		else:
			self._DESSTAT = 'NOT YET DESIGNED'		

	@property
	def OLD_WATTAGE(self):
		return self._OLD_WATTAGE
	@OLD_WATTAGE.setter
	def OLD_WATTAGE(self,value):
		if value not in ['NoSticker','OtherWattage']:
			self._OLD_WATTAGE = validateWattageValue(value)
		elif value == 'OtherWattage':
			self._OLD_WATTAGE = self.OTHER_WATTAGE
		else:
			self._OLD_WATTAGE = 'NO WATTAGE - REVIEW'

	def isValid(self):
		if self.TANKO_ID:
			return True
		else:
			return False

def validateWattageValue(value):
	#remove any characters that are not digits
	if value is not None:
		only_digits = re.sub('[^0-9]','', value)
	else:
		return None
	try:
		if only_digits:
			wattage = int(only_digits)
		else:
			return 'No wattage - REVIEW'
	except:
		return 'No wattage - REVIEW'
	return wattage