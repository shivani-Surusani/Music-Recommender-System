import songVectors as sv
import vectorSimilarity as vs
import unittest


class testfeatureVector(unittest.TestCase):
	knownValues = [(['user1','m','11','Japan','Oct'],[1,11,'Japan','Oct']),
									(['user1','','11','Japan','Oct'],[0,11,'Japan','Oct']),
									(['user1','f','None','Japan','Oct'],[-1,0,'Japan','Oct'])]
	def testCorrectOutput(self):
		"""songVector: featureVector should give correct output when called"""
		for i,o in self.knownValues:
			result = sv.featureVector(i)
			self.assertEqual(o,result)
	def testCorrectLength(self):
		"""songVector: featureVector should give correct length when called"""
		for i,o in self.knownValues:
			result = sv.featureVector(i)
			self.assertEqual(len(result),len(i)-1)
			
			
class testsongVectorToString(unittest.TestCase):
	knownValues = [({1:1,2:3},'1_1;2_3;'),
									({1:1},'1_1;'),
									({1:1,2:3,5:10},'1_1;2_3;5_10;')]
	def testCorrectOutput(self):
		"""songVector: songVectorToString should give correct output when called"""
		for i,o in self.knownValues:
			result = sv.songVectorToString(i)
			self.assertEqual(o,result)

class testfeatureVectorToString(unittest.TestCase):
	knownValues = [([1,'m','a','b'],'1;m;a;b;'),
									(['','m','a','b'],';m;a;b;'),
									(['None','NULL','a','b'],'None;NULL;a;b;')]
	def testNotListButTuple(self):
		"""songVector: featureVectorToString should fail if input is a tuple"""
		self.assertRaises(sv.listError,sv.featureVectorToString,(1,1))
	def testNotListButDictionary(self):
		"""songVector: featureVectorToString should fail if input is a dictionary"""
		self.assertRaises(sv.listError,sv.featureVectorToString,{1:1,2:2})
	def testCorrectOutput(self):
		"""songVector: featureVectorToString should give correct output when called"""
		for i,o in self.knownValues:
			result = sv.featureVectorToString(i)
			self.assertEqual(o,result)

		
class testparseVectorToDictionary(unittest.TestCase):
	knownValues = [('1_2;2_3',{'1':'2','2':'3'}),
									('1_2',{'1':'2'})]
	def testInputString(self):
		"""vectorSimilarity: parseVectorToDictionary should only take string input"""
		self.assertRaises(vs.songVectorError,vs.parseVectorToDictionary,{1:1,2:2})
		self.assertRaises(vs.songVectorError,vs.parseVectorToDictionary,[1,2])
	def testCorrectOutput(self):
		"""vectorSimilarity: parseVectorToDictionary should give correct output when called"""
		for i,o in self.knownValues:
			result = vs.parseVectorToDictionary(i)
			self.assertEqual(result,o)
			
class testparseVectorToList(unittest.TestCase):
	knownValues = [('2;m;Japan;Oct',['2','m','Japan','Oct']),
									('2;m;Oct',['2','m','Oct'])]
	def testInputString(self):
		"""vectorSimilarity: parseVectorToList should only take string input"""
		self.assertRaises(vs.featureVectorError,vs.parseVectorToList,{1:1,2:2})
		self.assertRaises(vs.featureVectorError,vs.parseVectorToList,[1,2])
	def testCorrectOutput(self):
		"""vectorSimilarity: parseVectorToList should give correct output when called"""
		for i,o in self.knownValues:
			result = vs.parseVectorToList(i)
			self.assertEqual(result,o)

			
class testfeatureSimilarity(unittest.TestCase):
	def testGenderBias(self):
		"""vectorSimilarity: featureSimilarity between vectors of same gender should me more than that of vectors between opposite gender"""
		result1 = vs.featuresimilarity(['1','10','INDIA','OCT 2016'],['1','10','INDIA','OCT 2016'])
		result2 = vs.featuresimilarity(['1','10','INDIA','OCT 2016'],['-1','10','INDIA','OCT 2016'])
		self.assertGreaterEqual(result1,result2)
	def testLocationBias(self):
		"""vectorSimilarity: featureSimilarity between vectors of same country should me more than that of vectors between different countries"""
		result1 = vs.featuresimilarity(['1','10','INDIA','OCT 2016'],['1','10','INDIA','OCT 2016'])
		result2 = vs.featuresimilarity(['1','10','INDIA','OCT 2016'],['1','10','JAPAN','OCT 2016'])
		self.assertGreaterEqual(result1,result2)

class testsongSimilarity(unittest.TestCase):
	def testSongBias(self):
		"""vectorSimilarity: songsimilarity between vectors of which have more songs in common with better rating each should have more similarity than in between those which are widely different"""
		result1 = vs.songsimilarity({1:10,2:20},{1:10,2:20})
		result2 = vs.songsimilarity({1:20,2:10},{1:10,2:20})
		self.assertGreaterEqual(result1,result2)
	def testNumberOfSongBias(self):
		"""vectorSimilarity: songsimilarity between vectors of which have more songs in common should have more similarity than those with lesser common songs"""
		result1 = vs.songsimilarity({1:10,2:20,3:1},{1:10,2:20,3:2})
		result2 = vs.songsimilarity({1:10,2:20},{1:10,2:20,3:2})
		self.assertGreaterEqual(result1,result2)

class testSimilarity(unittest.TestCase):
	def testRealData1(self):
		"""vectorSimilarity: similarity of {1:10,2:20},['1','10','INDIA','OCT 2016'] with {1:10,2:20},['1','10','INDIA','OCT 2016']  is clearly more then similarity with {1:20,2:10},['-1','10','JAPAN','OCT 2016']"""
		result1 = vs.vectorSimilarity('1_10;2_20','1_10;2_20',"1;10;INDIA;OCT 2016","1;10;INDIA;OCT 2016",0.95)
		result2 = vs.vectorSimilarity('1_10;2_20','1_20;2_10',"1;10;INDIA;OCT 2016","-1;10;JAPAN;OCT 2016",0.95)
		self.assertGreaterEqual(result1,result2)
		
	def testRealData2(self):
		"""vectorSimilarity: similarity of {1:10,2:20,3:1},['1','10','INDIA','OCT 2016'] with {1:10,2:20,3:2},['1','10','INDIA','OCT 2016']  is clearly more then similarity with {1:20,2:10},['1','10','JAPAN','OCT 2016']"""
		result1 = vs.vectorSimilarity('1_10;2_20;3_1','1_10;2_20;3_2',"1;10;INDIA;OCT 2016","1;10;INDIA;OCT 2016",0.95)
		result2 = vs.vectorSimilarity('1_10;2_20','1_20;2_10;3_2',"1;10;INDIA;OCT 2016","1;10;JAPAN;OCT 2016",0.95)
		self.assertGreaterEqual(result1,result2)
if __name__=="__main__":
	unittest.main()


