import json
from flask import Flask, render_template, request
import requests


app = Flask(__name__)
@app.route('/')
def homepage():
    return render_template('homepage.html')
@app.route('/', methods=['POST'])
def displaypage():
    searchquery =request.form['searchquery'] #gets the input from the form
    mydata =requests.get('https://youtube.googleapis.com/youtube/v3/search?part=snippet&q='+ searchquery +'&key=AIzaSyDeZHmbSdmiNyHJykeTLF2-LckM1toy6MQ')
    md = mydata.json()
    items = md['items']
    data = []
    for i in range(5): #loop which loops through each item in the items array, gets the title and videoId, proceeds to make an api call to get the comment and adds it to the comment array. Does this 5 times through, producing exactly 5 comments, one for each video.
        commentarray = []
        element = []
        element.append(items[i]['snippet']['title'])
        element.append(items[i]['id']['videoId'])
        commentdata = requests.get('https://youtube.googleapis.com/youtube/v3/commentThreads?part=snippet%2Creplies&videoId='+ items[i]['id']['videoId'] + '&key=AIzaSyDeZHmbSdmiNyHJykeTLF2-LckM1toy6MQ')
        for j in range(3):
            commentarray.append(json.loads(commentdata.content)['items'][j]['snippet']['topLevelComment']['snippet']['textDisplay'])
            j+=1
        element.append(commentarray)
        data.append(element)
        i+=1
    return render_template('commentspage.html', data = data)
    #return render_template('datapage.html', link1 = 'https://www.youtube.com/watch?v=' + videoidarray[0], videoid2 = 'https://www.youtube.com/watch?v=' + videoidarray[1], videoid3 = 'https://www.youtube.com/watch?v=' + videoidarray[2], videoid4 = 'https://www.youtube.com/watch?v=' + videoidarray[3], videoid5 = 'https://www.youtube.com/watch?v=' + videoidarray[4], videocomment= commentarray[0], videocomment1= commentarray[1], videocomment2= commentarray[2], videocomment3= commentarray[3], videocomment4= commentarray[4],  title= titlearray[0], title1= titlearray[1], title2= titlearray[2], title3= titlearray[3], title4= titlearray[4])

if __name__ == '__main__':
    app.run(debug=True)
