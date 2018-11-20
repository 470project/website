'''
* Recommender 
* jaccard similarity and then grab the highest ratings from the most similar users as long as those have never been rated by the target user.
'''

#read json file
import json

#importing app so global variables can be used
import app
from collections import OrderedDict

import pageRankRecommender

#user that we are matching
#matchUser = ["/u/1138361/iheartmwpp", "/u/8545331/Professor-Flourish-and-Blotts", "/u/4286546/Missbexiee", "/u/1697963/lydiamaartin", "/u/609412/Crystallic-Rain"]
def recommender(matchUser, userFavs, topStories):          

    #Find similar users
    jaccardDict = {}

    for key in userFavs:
        cInter = 0
        cUnion = len(matchUser)
        for author in userFavs[key]:
            if author in matchUser:
                cInter+=1
            else:
                cUnion+=1
                
        jaccardDict[key] = cInter/cUnion

    #Sorting Jaccard Dictionary    
    sortedJaccard = sorted(jaccardDict.items(), key=lambda kv: kv[1], reverse=True)
        
    authorsToLookAt = []
    authorStoryScore = {}

    #top twenty most similar
    for i in range(20):
        favList = userFavs[sortedJaccard[i][0]]
        for elem in favList:
            if elem not in matchUser:
                if elem in authorStoryScore:
                    #adds the similarity score to the previous score that way authors that show up multiple times have their weight increased.
                    #Not the best way to add but yolo
                    newSim = authorStoryScore[elem][0] + sortedJaccard[i][1]
                    authorStoryScore[elem] = (newSim, "")
                else:
                    authorsToLookAt.append(elem)
                    authorStoryScore[elem] = (sortedJaccard[i][1], "")        #saves the similarity score from the user and leaves the storylink blank for now.

    for elem in set(authorsToLookAt):
        if elem in topStories:
            simScore = authorStoryScore[elem][0]
            authorStoryScore[elem] = (simScore, topStories[elem][0])

    sortedDict = OrderedDict(sorted(authorStoryScore.items(), key=lambda kv: kv[1], reverse=True))

    return sortedDict

    '''
    j = json.dumbs(authorStoryScore)
    returnStr = ""
    returnStr += "Printing Author similarityScore story link.\n"
    for key in authorStoryScore:
        returnStr += str(key) + " " +  str(authorStoryScore[key][0]) + " " + str(authorStoryScore[key][1]) + "\n"
    return returnStr
    '''

#PRRec = pageRankRecommender(stories, users)
