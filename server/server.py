from flask import Flask, request, jsonify
import subprocess
import json
import re
from flask_cors import CORS

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

app = Flask(__name__)

cors = CORS(app)

@app.route('/player_batting', methods = ['GET'])
def index():
    pid = request.args.get('pid')
    sid = request.args.get('sid')
    if pid == None:
        return "No pid specified, try again"
    if sid == None:
        return "No sid specified, try again"

    url = "https://gc.com/t/{sid}/p/{pid}".format(sid=sid, pid=pid)
    bash_command = "curl -H 'Host: gc.com' -H 'Cookie: csrftoken=FTwt4ClWwRfJEggdpHQDL6faiC0i36fQ; hblid=lCP3gGLBFZZL7tV89R2zq0UGboS3AaDa; _okdetect=%7B%22token%22%3A%2215729662989550%22%2C%22proto%22%3A%22https%3A%22%2C%22host%22%3A%22gc.com%22%7D; olfsk=olfsk9024119620230786; _ok=9726-526-10-2279; gcdotcom_secure_sessionid=yie9cx4j0dikjci2o8xqwjx7ry4hudq2; gcdotcom_sessionid=togagjtlbtzw4hpkb9wcf00y9b5pdgze; wcsid=zMA5tEMV6mv89B759R2zq0U3SDmG3Eab; _okbk=cd4%3Dtrue%2Cvi5%3D0%2Cvi4%3D1573048806643%2Cvi3%3Dactive%2Cvi2%3Dfalse%2Cvi1%3Dfalse%2Ccd8%3Dchat%2Ccd6%3D0%2Ccd5%3Daway%2Ccd3%3Dfalse%2Ccd2%3D0%2Ccd1%3D0%2C; _sp_ses.9212=*; _sp_id.9212=c3908f52-2022-472d-816d-18ceb9369778.1572966298.3.1573052710.1573049793.449a7d05-8bdb-4204-9b07-c9a7f189414d; last_team_viewed=5c86c0ac3df30cdf60000001; _oklv=1573053380530%2CzMA5tEMV6mv89B759R2zq0U3SDmG3Eab' -H 'upgrade-insecure-requests: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36' -H 'sec-fetch-user: ?1' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3' -H 'sec-fetch-site: same-origin' -H 'sec-fetch-mode: navigate' -H 'referer: https://gc.com/t/summer-2019/ferda-baseball-club-5c86c0ac3df30cdf60000001/stats' -H 'accept-language: en-US,en;q=0.9' --compressed '{url}'".format(url=url)
    output = subprocess.check_output(['bash','-c', bash_command])
    return soup_player_batting_stats(output, pid)

def soup_player_batting_stats(html, pid):
    categories = []
    data = {}
    soup = BeautifulSoup(html)
    table = soup.find("table")
    cats = table.find("thead").find_all("th")
    game_log = []

    for cat in cats:
        categories.append(cat.string.strip())

    for entry in table.find("tbody").find_all("tr"): # for each game
        formatted_cols = []
        cols = entry.find_all("td") # each column

        for col in cols: # for each column for a particular game
            if col.find("time") != None: # datetime
                formatted_cols.append(col.find("time")['datetime'])
            elif col.find("a") != None: # link value
                formatted_cols.append(col.find("a").string.strip())
            elif col.string != None: # value
                formatted_cols.append(col.string.strip())
            
        game_log.append( { category: col for category, col in zip(categories, formatted_cols) } )
    
    data["id"] = pid
    player_info = soup.find("h1", {"class": "giganticText mbs"}).get_text()
    data["name"] = re.split("#", player_info, 1)[0].strip()
    data["number"] = re.split("\s", re.split("#", player_info, 1)[1], 1)[0]
    data["positions"] = re.split("Ferda", re.split("\s", re.split("#", player_info, 1)[1], 1)[1], 1)[0].strip()
    data["games"] = game_log

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug = True)
