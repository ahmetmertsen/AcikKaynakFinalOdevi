import requests

class thePremierLeague:
    def __init__(self):
        self.api_url = "https://heisenbug-premier-league-live-scores-v1.p.rapidapi.com/api/premierleague/team"
        self.headers = {
            "x-rapidapi-key": "98d0bb17camsh0ced32eabca8c3dp158880jsn16decd0501fe",
	        "x-rapidapi-host": "heisenbug-premier-league-live-scores-v1.p.rapidapi.com"
        }


    def getTeam(self):
        querystring = {"name":"Liverpool"}
        response = requests.get(self.api_url, headers=self.headers,params=querystring)
        return response.json()
    
premierleaugeApi = thePremierLeague()
team = premierleaugeApi.getTeam()
bilgi = input(f"Görmek İstediğiniz {team['name']} Takımı Bilgisi: ")   
print(team[bilgi])

# Basit 2 request örenği; 
# managers: Teknik direktör bilgisi, 
# venue: Takım Stadı Adı

