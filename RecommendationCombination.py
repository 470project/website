import recommend
import pageRankRecommender as PRR
import recommenderSurprise as RS
import app
import json
import collections
from collections import Counter
import userInfo

class RecommendationCombination():
    def __init__(self, numEntities = 1000): 
        self.userFavs = {}
        self.topStories = {}
        self.stories = []
        self.users = []
        self.reviews = [] 
        with open('resultCleanup.jl') as f:   
            cnt = 0
            for line in f:
                if cnt > numEntities:
                    break
                cnt += 1
                j = json.loads(line)
                if j["pT"] == "user":
                    self.users.append(
                        {
                            'name':j['name'], 
                            'stories':j['stories'],
                            'favorites':j['favorites']
                        })
                    favAuthors = []
                    favs = j["favorites"]
                    for elem in favs:
                        favAuthors.append(elem["A"])
                    self.userFavs[j["name"]] = set(favAuthors)

                if j["pT"] == "story":
                    favs = int(j["otherInfo"]["favorites"])
                    author = j["author"]
                    link = j["storyLink"]
                    
                    self.stories.append({'storyLink':j["storyLink"]})

                    if author not in self.topStories:
                        self.topStories[author] = (link, int(favs))
                    else:
                        #if the current top story for the author has less favorites than the new story then make the new story the top story. else don't change anything.
                        if int(self.topStories[author][1]) < int(favs):
                            self.topStories[author] = (link, int(favs)) 
                if j["pT"] == "review":
                    item = {}
                    item['rO'] = j['rO']
                    item['r'] = j['r']
                    item['sS'] = j['sS']
                    self.reviews.append(item)

        self.prRecommender = PRR.pageRankRecommender(self.users, self.stories)
        self.sRecommender = RS.surpriseRecommender(self.stories, self.reviews, self.users)
        self.sRecommender.train()

    def getTopAuthors(self, link):

        favoriteAuthors = userInfo.getFavoriteAuthors(link)

        basicRecommendations = recommend.recommender(favoriteAuthors, self.userFavs, self.topStories)
        basicRecommendations = Counter({ x : y[0] for x, y in basicRecommendations.items()})
        pageRankRecommendations = Counter({link: score * .1 for link, score in self.prRecommender.predictBestAuthors().items()})

        combinedResults = dict(basicRecommendations + pageRankRecommendations)
        #print(len(basicRecommendations),len(pageRankRecommendations),len(combinedResults))
        combinedResults = [(link, score) for link, score in combinedResults.items()]
        combinedResults = sorted(combinedResults, key=lambda tup: tup[1], reverse=True)[:10]
        #print(combinedResults[:10])


        return [ x for x, y in combinedResults]

    def getTopStories(self, link):
        def scaleCounter(counter, scaler):
            return Counter({ link : score * scaler for link, score in counter.items()})

        pageRankRecommendations = Counter({link: score for link, score in self.prRecommender.predictBestStories().items()})
        pageRankRecommendations = scaleCounter(pageRankRecommendations, .1)
        surpriseRecommendations = Counter(self.sRecommender.predict(link, self.stories))
        surpriseRecommendations = scaleCounter(surpriseRecommendations, .9)

        combinedResults = pageRankRecommendations + surpriseRecommendations
        combinedResults = [(link, score) for link, score in combinedResults.items()]
        combinedResults = sorted(combinedResults, key=lambda tup: tup[1], reverse=True)[:10]
        print(combinedResults)
        return [ x for x, y in combinedResults]
