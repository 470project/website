from flask import Flask, redirect, render_template, url_for, request
#read json file
import json
import recommend
import userInfo
import json_lines
import pageRankRecommender as PRR
app = Flask(__name__)

#adding global variables
userFavs = dict()
topStories = dict()


@app.route('/')
def home():
    return render_template('fanfix.html')

@app.route('/fanfix.html/')
def back_to_same():
    return redirect(url_for('home'))

@app.route('/informationInput.html/')
def inputPage():
	return render_template('informationInput.html')

@app.route('/informationInput.html/informationInput.html/')
def back_to_informationInput():
    return redirect(url_for('inputPage'))

@app.route('/informationInput.html/fanfix.html/')
def back_to_home():
    return redirect(url_for('home'))

@app.route('/informationInput.html/recommendation.html', methods = ['POST','GET'])
def outputPage():
    if request.method == 'POST':
        link = request.form['link']
        #favoriteAuthors = ["/u/1138361/iheartmwpp", "/u/8545331/Professor-Flourish-and-Blotts", "/u/4286546/Missbexiee", "/u/1697963/lydiamaartin", "/u/609412/Crystallic-Rain"]
        favoriteAuthors = userInfo.getFavoriteAuthors(link)
        #result = recommend.recommender(favoriteAuthors)
        scores = [ (link, score)for link, score in prRecommender.predict().items()]
        result = scores[:10]
        print(result[:10])
        return render_template('recommendation.html', data=result[:10])
	
@app.route('/recommendation.html/fanfix.html/')
def back_to_home_rec():
    return redirect(url_for('home'))

@app.route('/recommendation.html/informationInput.html/')
def back_to_input_rec():
    return redirect(url_for('inputPage'))

def startup():
    global userFavs
    global topStories
    global stories, users
    global prRecommender
    stories = []
    users = []
    with app.open_resource('result.jl') as f:  
        for line in f:
            j = json.loads(line)
            if j["pageType"] == "user":
                users.append({'name':j['name'], 'stories':j['stories']})
                favAuthors = []
                favs = j["favorites"]
                for elem in favs:
                    favAuthors.append(elem["favAuthor"])
                userFavs[j["name"]] = set(favAuthors)

            if j["pageType"] == "story":
                favs = int(j["otherInfo"]["favorites"])
                author = j["author"]
                link = j["storyLink"]
                
                stories.append({'storyLink':j["storyLink"]})

                if author not in topStories:
                    topStories[author] = (link, int(favs))
                else:
                    #if the current top story for the author has less favorites than the new story then make the new story the top story. else don't change anything.
                    if int(topStories[author][1]) < int(favs):
                        topStories[author] = (link, int(favs))   
    prRecommender = PRR.pageRankRecommender()
    
startup()

@app.route('/karl/')
def karlTest():
    matchUser = ["/u/1138361/iheartmwpp", "/u/8545331/Professor-Flourish-and-Blotts", "/u/4286546/Missbexiee", "/u/1697963/lydiamaartin", "/u/609412/Crystallic-Rain"]  #these are the authors that the user has favorited
    return json.dumps(recommend.recommender(matchUser))    #isn't a string right now so flask will dislike.

@app.route('/daniel/')
def danielTest():
    userName = "Basketbears"
    userId = "5253296"
    userURL = "https://www.fanfiction.net/u/5253296/Basketbears"
    userPage = requests.get(userURL)
    return userPage
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
