import recommend
import pageRankRecommender as PRR

import app

def getTopAuthors(favoriteAuthors):
    result = recommend.recommender(favoriteAuthors)
    scores = [ link for link, score in app.prRecommender.predict().items()]
    #result = scores[:10]
    print(result[:10])

    return result
