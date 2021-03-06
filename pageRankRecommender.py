import json
import string
import json_lines
import itertools
import re
import app

class pageRankRecommender():
    def __init__(self, users, stories):
        with open('PRresult.json') as f:
            PRresults = json.load(f)

        userLinkToIdDict = {}
        IdToUserDict = {}

        lastUserId = 0
        for user in users:
            userLinkToIdDict[user['name']] = lastUserId
            IdToUserDict[lastUserId] = user
            lastUserId += 1

        storyLinkToIdDict = {}
        IdToStoryDict = {}

        shortStoryIds = []

        def getShortStoryId(link):
            #/s/4536005/1/Oh-God-Not-Again
            m = re.match('/s/(?P<shortId>\d+)/\d', link)
            if(m is None):
                return ""
            return m.group('shortId')

        #create a dict between storied and their id
        lastStoryId = 0
        for story in stories:
            shortId = getShortStoryId(story['storyLink'])
            if(shortId not in shortStoryIds):
                shortStoryIds.append(shortId)
            else:
                continue
            storyLinkToIdDict[story['storyLink']] = lastStoryId
            IdToStoryDict[lastStoryId] = story
            lastStoryId += 1
        
        self.storyLinkToScores = {}
        self.userLinkToScores = {}

        minScore = 0
        maxScore = 0

        for res in PRresults:
            score = res['score']
            minScore = min(score, minScore)
            maxScore = max(score, maxScore)
        print(minScore, maxScore)
        delta = maxScore - minScore
        scale = 1 / delta 

        for res in PRresults:
            score = res['score'] / delta
            link = res['link']

            self.userLinkToScores[link] = score

            if(link in userLinkToIdDict):
                user = IdToUserDict[userLinkToIdDict[link]]
                for story in user['stories']:
                    if(story in storyLinkToIdDict):
                        self.storyLinkToScores[story] = score

    def predictBestStories(self):
        return self.storyLinkToScores

    def predictBestAuthors(self):
        return self.userLinkToScores
'''
#%%

with open('result.jl', 'rb') as f:
    entities = [x for x in json_lines.reader(f)][:100000]
    stories = [x for x in entities if str(x['pageType']) == "story" and str(x['storyType']) == '/book/Harry-Potter/']
    users = [x for x in entities if str(x['pageType']) == "user"]

#%%
PRRec = pageRankRecommender(stories, users)
scores = [ (link, score)for link, score in PRRec.predict().items()]

#print(scores[:10])
print(sorted(scores, key=lambda tup: tup[1],reverse=True)[:10])
'''

