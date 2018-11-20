from flask import Flask, redirect, render_template, url_for, request
#read json file
import json
import recommend
import userInfo
import json_lines
import pageRankRecommender as PRR
import RecommendationCombination as RC
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
        
        result = json.dumps(
            {
                'authors' : recommender.getTopAuthors(link),
                'stories' : recommender.getTopStories(link) 
            })
        return render_template('recommendation.html', data=result)

	
@app.route('/recommendation.html/fanfix.html/')
def back_to_home_rec():
    return redirect(url_for('home'))

@app.route('/recommendation.html/informationInput.html/')
def back_to_input_rec():
    return redirect(url_for('inputPage'))

@app.route('/karl/')
def karlTest():
    matchUser = ["/u/1138361/iheartmwpp", "/u/8545331/Professor-Flourish-and-Blotts", "/u/4286546/Missbexiee", "/u/1697963/lydiamaartin", "/u/609412/Crystallic-Rain"]  #these are the authors that the user has favorited
    return json.dumps(recommend.recommender(matchUser))    #isn't a string right now so flask will dislike.

recommender = 0

if __name__ == "__main__":
    ctx = app.app_context()
    recommender = RC.RecommendationCombination()
    ctx.push()
    app.run(host='0.0.0.0', debug=True)

    
    
    
