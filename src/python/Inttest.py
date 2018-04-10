import songVectors as sv
import vectorSimilarity as vs
import unittest

class testfeatureVector(unittest.TestCase):
	knownValues = [(['user1','m','11','Japan','Oct'],[1,11,'Japan','Oct']),
									(['user1','','11','Japan','Oct'],[0,11,'Japan','Oct']),
									(['user1','f','None','Japan','Oct'],[-1,0,'Japan','Oct'])]
	def testNotDictionary(self):
		"""songVector: featureVector should fail if input is a dictionary"""
		self.assertRaises(sv.dictError,sv.featureVector,{1:1,2:2})

class testsongVectorToString(unittest.TestCase):
	knownValues = [({1:1,2:3},'1_1;2_3;'),
									({1:1},'1_1;'),
									({1:1,2:3,5:10},'1_1;2_3;5_10;')]
	def testNotDictionaryButTuple(self):
		"""songVector: songVectorToString should fail if input is a tuple"""
		self.assertRaises(sv.dictError,sv.songVectorToString,(0,0,1))
	def testNotDictionary(self):
		"""songVector: songVectorToString should fail if input is a list"""
		self.assertRaises(sv.dictError,sv.songVectorToString,[0,0,1])

class testfeatureSimilarity(unittest.TestCase):
	def testInputString(self):
		"""vectorSimilarity: inputs to featureSimilarity should both input of same size"""
		self.assertRaises(vs.featurelengthError,vs.featuresimilarity,[1,2],[2])

class testsongSimilarity(unittest.TestCase):
	def testInputDict(self):
		"""vectorSimilarity: inputs to songsimilarity should both be dictionaries"""
		self.assertRaises(vs.songdictError,vs.songsimilarity,{1:2},[2])

if __name__=="__main__":
	unittest.main()



