# website

This is the Fan fiction website.

you will need to have flask and requests installed to run this project.

to run use python3.6 app.py.

The main areas of interest are 

## static

holds all of the static webpage assets

## app.py

this holds the driver code for the website

## RecommendationCombination.py

takes all of the recommenders and squishes their results into one big one

## recommend.py

this is theauthor recommender using collaberative filtering

## pageRankRecommender.py

this is the basline story recommender using page rank

## recommenderSurprise.py

this is the recommender code for the SVD recommender using the surprise library

## userInfo.py

scrapes the user info for new requests
