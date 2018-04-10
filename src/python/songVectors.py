class svError(Exception): pass
class dictError(svError): pass
class listError(svError): pass
class lengthError(svError): pass
def featureVector(s):
	if isinstance(s,dict):
		raise dictError, "input must not be a dictionary"
		
	v = [0,0,0,0] #Sex,Age,Country,Date Joined
	if(s[1]=='m'):
		v[0]=1
	if(s[1]=='f'):
		v[0]=-1
	if(s[2] and str(s[2]).isdigit()):
		v[1]=int(s[2])
	v[2]=s[3]
	v[3]=s[4]
	
	if(len(v) != len(s)-1):
		raise lengthError, "output not of correct length"
	return v
	
def songVectorToString(v):
	if not isinstance(v,dict):
		raise dictError, "input must be a dictionary"
	s=''
	for key,item in v.items():
		s= s + str(key)+'_'+str(item)+';'
	return s

def featureVectorToString(v):
	if not isinstance(v,list):
		raise listError, "input must be a list"
	s=''
	for item in v:
		s=s+str(item)+';'
	return s
