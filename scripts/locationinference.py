import glob
import orjson
import csv

from twitwhere.geoguess.geoguess import geoguess_in_target
from twitwhere.geoguess import geoguess
#from geoguess import geoguess, init
from shapely.geometry import box
from shapely.geometry import GeometryCollection
from shapely.ops import nearest_points
from tqdm import tqdm 
import time
import urllib.request
import os
""""
init(uk=True, use_geonames=True, use_dbpedia=True)

from info import countries
	
target_area = box( *countries["united kingdom"] ).buffer(0.1)
target_area_names = {"united kingdom"}
"""

db_weights = {'dbpedia': 1, 'naturalearth': 1, 'geonames_1000': 0.5}
weights = {'text': 2, 'location': 1, 'url': 1, 'profile': 1, 'description': 0}

ids = []
times = []
text = []
polys = []
media = []
media_count = []

pics = []
for f in sorted(glob.glob("/home/joyce/Projects/Flood_Tweet_Project/data/Tweets/RelevantTweets/*.json")):
    with open(f) as infile:
        print(infile)
        for line in infile:
            try:
                tweet = orjson.loads(line)
            except orjson.JSONDecodeError:
                pass
            if 'id_str' in tweet and(not tweet['is_quote_status']):
                polygon = geoguess_in_target(tweet, target_countries = ['united kingdom'], db_weights=db_weights, weights=weights)
                if polygon:

                    polys.append(polygon[0])
                    ids.append(tweet["id_str"])
                    times.append(tweet["created_at"])
                    if 'extended_tweet' in tweet:
                        text.append(tweet["extended_tweet"]["full_text"])
                    else:
                        text.append(tweet["text"])
                    try:
                        media += tweet['extended_entities']['media']
                        media_count.append(1)
                    except:pass

rows = zip(ids, times, text, polys)

header = ['id', 'time', 'tweet', 'polygon']
with open('../data/Tweets/location_inferred_tweets/location_inferred_tweets.csv', 'w', newline = "") as myfile:
	writer = csv.writer(myfile)
	writer.writerow(i for i in header)
	for row in rows:
		writer.writerow(row)
"""
for ids, media in zip(ids,media):
    for media in media['media']:
        if media['type'] == 'photo':
            pics.append(ids, media['media_url'])
    #pics.append([ids,media['media_url']])


failed = []
for pic in tqdm(pics):
    
     #setting filename and image URL
    filename = f"/home/joyce/filtered_tweets_test/Complete_Tweets/Flood_Images/{pic[0]}.jpg"
    if os.path.exists(filename):continue

    try:
        #calling urlretrieve function to get resource
        urllib.request.urlretrieve(pic[1], filename)
    except:
        failed.append(pic)
        
    time.sleep(1)

print(len(failed))
"""
