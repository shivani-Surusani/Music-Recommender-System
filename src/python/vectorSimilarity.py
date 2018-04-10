import math
class svError(Exception): pass
class dictError(svError): pass
class listError(svError): pass
class songdictError(svError): pass
class featurelengthError(svError): pass
class featureVectorError(svError): pass
class songVectorError(svError): pass
def pearsonSimilarity(s1,s2,f1,f2,alpha):
	 #alpha Parameter to control how much weightage to give artist or features
	s1=parseVectorToDictionary(s1);
	s2=parseVectorToDictionary(s2);
	f1=parseVectorToList(f1);
	f2=parseVectorToList(f2);
	return(alpha*pearsonsongsimilarity(s1,s2)+(1-alpha)*featuresimilarity(f1,f2))
	
def vectorSimilarity(s1,s2,f1,f2,alpha):
	 #alpha Parameter to control how much weightage to give artist or features
	s1=parseVectorToDictionary(s1);
	s2=parseVectorToDictionary(s2);
	f1=parseVectorToList(f1);
	f2=parseVectorToList(f2);
	return(alpha*songsimilarity(s1,s2)+(1-alpha)*featuresimilarity(f1,f2))

def pearsonsongsimilarity(s1,s2):
	if not isinstance(s1,dict) or not isinstance(s2,dict):
		raise songdictError, "songVectors must be dictionaries"
	total=0.0
	s1total=0.0
	s2total=0.0
	s1avg=0.0
	s2avg=0.0
	count=0
	for key,item in s1.items():
		s1avg+=float(item)
		count+=1
	s1avg=s1avg/count
	count=0
	for key,item in s2.items():
		s2avg+=float(item)
		count+=1
	s2avg=s2avg/count
	for key,item in s1.items():
		s1total+=(float(item)-s1avg)*(float(item)-s1avg)
	for key,item in s2.items():
		s2total+=(float(item)-s2avg)*(float(item)-s2avg)
		if key in s1:
			total+=(float(item)-s2avg)*(float(s1[key])-s1avg)
	return total/math.sqrt(s1total*s2total+0.0000001)
	
def songsimilarity(s1,s2):
	if not isinstance(s1,dict) or not isinstance(s2,dict):
		raise songdictError, "songVectors must be dictionaries"
	total=0.0
	s1total=0.0
	s2total=0.0
	for key,item in s1.items():
		s1total+=float(item)*float(item)
	for key,item in s2.items():
		s2total+=float(item)*float(item)
		if key in s1:
			total+=float(item)*float(s1[key])
	return total/math.sqrt(s1total*s2total)
	
def featuresimilarity(f1,f2):
	if(len(f1)!=len(f2)):
		raise featurelengthError, "featureVectors must be of same length"
	genderWeight=0.1;
	LocationWeight=1;
	total=0.0
	total+=float(f1[0])*float(f2[0])*genderWeight
	if(f1[2]==f2[2]):
		total+=LocationWeight
	return total

def parseVectorToDictionary(v):
	if not isinstance(v, basestring):
		raise songVectorError, "pass a song vector as string"
	songdict={}
	v=v.split(';')
	for k in v:
		k=k.split('_')
		if(len(k)>1):
			songdict[k[0]]=k[1]
	return songdict

def parseVectorToList(v):
	if not isinstance(v, basestring):
		raise featureVectorError, "pass a feature vector as string"
	songlist=[]
	v=v.split(';')
	for k in v:
		if(len(k)>0):
			songlist.append(k)
	return songlist
