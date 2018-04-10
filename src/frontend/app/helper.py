def songdata(songs,indices,songvector):
	indexDict={}
	for (a,b) in indices:
		indexDict[b]=a
	songdict={}
	songvector=songvector.split(';')
	for k in songvector:
		k=k.split('_')
		if(len(k)>1):
			songdict[k[0]]=k[1]
	songlist=[]
	checksongs={}
	for song in songs:
		if song[0] not in checksongs:
			checksongs[song[0]]=1
			songlist.append((song[1],song[2],songdict[str(indexDict[song[0]])]))
	songlist.sort(key=lambda tup: int(tup[2]), reverse=True) 
	return songlist
