import math
import copy
import random

xfactor=10

def normalize(R,factor):
	X=copy.deepcopy(R)
	for i, l in X.iteritems():
		for ss in l:
			X[i][ss]=1000.0*((2.0/(1.0+math.exp(-factor*float(X[i][ss])))) -1.0)
			#~ X[i][ss]=X[i][ss]*factor
	return X
def EM(listeningHistory,flag,normalizer):
	
	
	Yus = normalize(listeningHistory,normalizer)
	Rus = normalize(listeningHistory,normalizer*1.05)
	
	if(flag==0):
		#~ print Yus
		return Yus
	if(flag==2):
		return listeningHistory
	Rusp={} #previous value of Rus
	mus='mus'
	dvs='dvs'
	muu='muu'
	dvu='dvu'
	
	def expectations(nu,ns,sngl):
		#sum1 is for myu of song sum2 for deviation of song Sum3 myu of user sum4 deviation of user
		q=1
		count=1
		while q==1:
			print count
			count+=1
			Exsng={} # a dictionary which stores mu and deviation of each song
			Exusr={} # a dict which stores mu and deviation of each user
			for ss in sngl:
					sum1=0.0
					ns=0.0
					if Exsng.has_key(ss):
						continue
					Exsng[ss]={}
					for x,y in Rus.iteritems():
						if y.has_key(ss):
							sum1+=Rus[x][ss]
							ns+=1
					Exsng[ss][mus]=sum1/ns
			for ss in Exsng:
				sum2=0.0
				ns=0.0
				for x,y in Rus.iteritems():
					if y.has_key(ss):
						sum2+= (Rus[x][ss]-Exsng[ss][mus])**2
						ns+=1
				#~ if(ns>1):
					#~ print (sum2,sum2/ns)
				Exsng[ss][dvs]=math.sqrt(sum2/(ns)) + 10000
			for u, s in Rus.iteritems():
				sum3=0.0
				nu=0.0
				if Exusr.has_key(u):
					continue
				Exusr[u]={}
				for ss in s:
					sum3+=Rus[u][ss]
					nu+=1
				Exusr[u][muu]=sum3/nu
			for u in Exusr:
				sum4=0.0
				nu=0.0
				for ss in Rus[u]:
					sum4+= (Rus[u][ss]-Exusr[u][muu])**2
					nu+=1
				#~ print (sum4,sum4/nu)
				Exusr[u][dvu]=math.sqrt(sum4/(nu))
			Rusp=copy.deepcopy(Rus)
			Maximisation(Exsng,Exusr)
			if comp(Rus,Rusp):
				q=0
				#~ print Exsng
				#~ print Exusr
		#~ print Rus
		return Rus
		
		
		
	def Maximisation(sa,ua):
		for u,s in Rus.iteritems():
			for ss in s:
				if((sa[ss][dvs]**2+ua[u][dvu]**2)>0):
					newval=((sa[ss][dvs]**2)*ua[u][muu]+(ua[u][dvu]**2)*sa[ss][mus]+xfactor*(max(1,(ua[u][dvu]**2)*(sa[ss][dvs]**2)))*Yus[u][ss])/(sa[ss][dvs]**2+ua[u][dvu]**2+xfactor*max(1,(ua[u][dvu]**2)*(sa[ss][dvs]**2)))
				else:
					newval = Yus[u][ss]
				
				Rus[u][ss]=Rus[u][ss] + 0.5*(newval-Rus[u][ss])
		return 



	def comp(A,B):
		for u,s in A.iteritems():
			for ss in s:
				if abs(A[u][ss]-B[u][ss])>0.05:
					print abs(A[u][ss]-B[u][ss])
					return False
		return True
					

	nu= len(Rus)
	ns=0
	sl=[]
	DR={}
	for i, l in Rus.iteritems():
		for song in l:
			if song not in sl:
				sl.append(song)
	ns=len(sl)
	DR=expectations(nu,ns,sl); #Derived ratings

	#~ for i, l in DR.iteritems():
		#~ for ss in l:
			#~ print ("user "+str(i)+" song "+str(ss)+" ratings are "+str(DR[i][ss]) + " prev: " + str(Yus[i][ss]))
	return DR

