from flask import Flask, redirect, render_template, url_for
#read json file
import json

app = Flask(__name__)

#adding global variables
userFavs = dict()
topStories = dict()




@app.route('/')
def hello():
    return render_template('fanfix.html')

@app.route('/informationInput.html/')
def hello_world():
	return render_template('recommendation.html')

@app.route('/informationInput.html/informationInput.html/')
def back_to_informationInput():
    return redirect(url_for('hello_world'))

@app.route('/informationInput.html/fanfix.html/')
def back_to_home():
    return redirect(url_for('hello'))

def startup():
    global userFavs
    global topStories

    with app.open_resource('result.jl') as f:  
        for line in f:
            j = json.loads(line)
            if j["pageType"] == "user":
                favAuthors = []
                favs = j["favorites"]
                for elem in favs:
                    favAuthors.append(elem["favAuthor"])
                userFavs[j["name"]] = set(favAuthors)

            if j["pageType"] == "story":
                favs = int(j["otherInfo"]["favorites"])
                author = j["author"]
                link = j["storyLink"]
                if author not in topStories:
                    topStories[author] = (link, int(favs))
                else:
                    #if the current top story for the author has less favorites than the new story then make the new story the top story. else don't change anything.
                    if int(topStories[author][1]) < int(favs):
                        topStories[author] = (link, int(favs))
    
    
startup()

@app.route('/karl/')
def karlTest():
    return str(len(userFavs))


if __name__ == "__main__":
    app.run()
