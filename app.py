import requests
import re


from flask import Flask,jsonify
app = Flask(__name__)


class WebScrape:
    URL = 'https://www.time.com'
    def getResponse(self):
        response = requests.get(self.URL)
        responseString = str(response.text)
        return responseString
    def getStoriesTitleandLink(self):
        responseString = self.getResponse()
        indexPartialStories = responseString.find('partial latest-stories')
        responseString = responseString[indexPartialStories:indexPartialStories + 14000]
        title = re.findall('<h3[^>]*>(.*?)</h3>', responseString)
        link = re.findall('href="/([^"]*)"[^>]*>([\s\S]*?)</a>', responseString)
        requiredLinkArray = []
        for i in range(len(link)):
            requiredLinkArray.append(link[i][0])
        return(title,requiredLinkArray)




@app.route('/getTimeStories', methods=['GET'])
def getTimeStories():
    data = WebScrape().getStoriesTitleandLink()
    requiredJson = []
    for i in range(len(data[0])):
        jsonMap = {'title': data[0][i], 'link': data[1][i]}
        requiredJson.append(jsonMap)
    return jsonify(requiredJson)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
