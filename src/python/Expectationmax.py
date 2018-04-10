#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Expectationmax.py
import math
class myclass:
	
	global Yus={U1:{s1:7,s3:3,s5:4,s7:10,s9:1},U2:{s2:1,s4:2.5,s6:4.5,s8:5.5,s10:8},U3:{s1:10,s2:9,s3:8,s4:8.5,s5:8},U4:{s6:1.5,s7:2.5,s8:3,s9:4.5,s10:2},U5:{s3:3,s6:6.5,s7:9.5,s4:3.5,s5:10}}
	global Rus=Yus
	global DetrRus={}
	global rusp={} #previous value of Rus
	
	def expectations(nu,ns)
		#sum1 is for myu of song sum2 for deviation of song Sum3 myu of user sum4 deviation of user
		While q=1
			Exsng={} # a dictionary which stores mu and deviation of each song
			Exusr={} # a dict which stores mu and deviation of each user
			for u, s in DetrRus.iteritems():
				for ss in s:
					sum1=0.0
					if Exsng.has_key(ss):
						continue
					for x,y in Rus.iteritems():
						if y.has_key(ss):
							sum1+=Rus[x][ss]
					Exsng[ss][mus]=sum1/ns
			for ss in Exsng:
				sum2=0.0
				for x,y in Rus.iteritems():
					if y.has_key(ss):
						sum2+= (Rus[x][ss]-Exsng[ss][mus])**2
				Exsng[ss][dvs]=math.sqrt(sum2)/(ns-1)
			for u, s in Rus.iteritems():
				sum3=0.0
				if Exusr.has_key(u):
					continue
				for ss in s:
					sum3+=Rus[u][ss]
				Exusr[u][muu]=sum3/nu
			for u in Exusr:
				sum4=0.0
				for ss in Rus[u]:
					sum4+= (Rus[u][ss]-Exusr[u][muu])**2
				Exusr[u][dvu]=math.sqrt(sum4)/(nu-1)
			DetrRus=Maximisation(Exsng,Exusr);
			if comp(DetrRus,Rusp):
				q=0
			Rus=Yus.update(DetrRus)
		return DetrRus
	def Maximisation(Sa,Ua)
		T=DetrRus
		for u,s in T:
			for ss in s:
				T[u][ss]=((sa[ss][dvs]**2)*Yus[u][ss]+(ua[u][dvu]**2)*sa[ss][mus])/(sa[ss][dvs]**2+ua[u][dvu]**2)
		Rusp=DetrRus
		return T
	def comp(A,B)
		for u,s in A:
			for ss in s:
				if abs(A[u][ss]-b[u][ss])>0.001:
					return false
		return true
				
	def main(args):
		nu= len(Rus)
		ns=0
		sl=[]
		for i, l in Rus.iteritems():
			for song in l:
				if song not in sl:
					sl.append(song)
		ns=len(sl)
		for x, y in Yus.iteritems():
			for s in sl:
				if !(y.has_key(s)):
					DetrRus[x][s]=0;
		DR=expectations(nu,ns); #Derived ratings
		for i, l in DR:
			for ss in l:
				print ("user %s"+i+"song %s"+ss+"ratings are %f"+DR[i][ss])
	
	if __name__ == '__main__':
		import sys
		sys.exit(main(sys.argv))
