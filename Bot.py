import apiai, json

class Bot:
    def __init__(self, token, lang, session_id):
        self.request = apiai.ApiAI(token).text_request()
        self.request.lang = lang
        self.request.session_id = session_id
    
    def send_msg(self, msg):
        self.request.query = msg
        response = json.loads(self.request.getresponse().read().decode("utf-8"))
        print(f"////////////////////\n{response['result']}\n///////////////////")
        try:
            intent = response['result']['metadata']['intentName']
            parameters = response['result']['parameters']
        except:
            intent = ""
            parameters = {}
        response = response['result']['fulfillment']['messages']
        needToSay = ""
        for item in response:
            needToSay += f"{item['speech']}\n"
        return needToSay, intent, parameters

    
