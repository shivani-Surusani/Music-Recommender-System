import csv
with open('../../data/userid-profile.tsv','r') as users:
	users=csv.reader(users,delimiter='\t')
	out=open('../../data/userid-profile-trim.tsv','w')
	temp=next(users)
	#~ print temp
	out.write('\t'.join(temp)+'\n')
	for user in users:
		if(int((user[0].split('_'))[1])<150):
			#~ print '\t'.join(user)
			out.write('\t'.join(user)+'\n')
import sys
with open('../../data/userid-timestamp-artid-artname-traid-traname.tsv','rb') as users:
	#csv.field_size_limit(2147483647)
	users=csv.reader(users,delimiter='\t',quoting=csv.QUOTE_NONE)
	out=open('../../data/userid-timestamp-artid-artname-traid-traname-trim.tsv','w')
	temp=next(users)
	#~ print temp
	out.write('\t'.join(temp)+'\n')
	for user in users:
		if(int((user[0].split('_'))[1])<150):
			#~ print '\t'.join(user)
			out.write('\t'.join(user)+'\n')
