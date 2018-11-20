import recommend
import pageRankRecommender as PRR

import app

def getTopAuthors(favoriteAuthors):
    result = recommend.recommender(favoriteAuthors)
    scores = [ (link, score) for link, score in app.prRecommender.predictBestAuthors().items()]
    #result = scores[:10]
    print(scores[:10])
    print(result)
    return result
