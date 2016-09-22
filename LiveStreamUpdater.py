import re, io, json, requests, praw, OAuth2Util, configparser
# Reads and sets up config
config = configparser.ConfigParser()
config.read("config.ini")
retrieveLive = config["settings"]["retrieveLive"]
# This is the API link for twitch. All calls to the api start with this.
api_link = "https://api.twitch.tv/kraken/streams"
 
# The main big boy function 
def retrieveList():
    # Setup Reddit connection. Read README.md for instructions on how to setup OAuth2
    def reddit_Setup(subreddit):
        print("Connecting to reddit.")
        user_agent = "Auto Update livestreamers for /r/{} ".format(subreddit)
        r= praw.Reddit(user_agent=user_agent)
        o= OAuth2Util.OAuth2Util(r)
        # Automatic refreshing the OAuth2 key
        o.refresh(force=True)
        sub = r.get_subreddit(subreddit)
        return r, sub
    
    # Now let's get those streamers!
    def new_streamsDef(data):   
        streamsARR = []
        # This will grab 20~ streamers max, 
        # A sidebar with more than 20 streamers on it is a sidebar I don't want to see
        for streamer in data["streams"]:
            replacedstreamer = streamer["channel"]["display_name"]
            try: 
                streamsARR.append(replacedstreamer)
            except KeyError:
                pass
        return streamsARR
    # Now lets write to the wiki
    def post_toReddit(sub, newStreams):
        sub.edit_wiki_page(
           "streams",
           "\n".join(newStreams),
           reason="Updated Currently Live Streams" 
           )
    # More configs!
    subreddit = config["settings"]["subreddit"]
    game = config["settings"]["game"]
    clientID = config["settings"]["clientID"]
    parse = {"game" : game, "client_id" : clientID}
    # This converts your pesky spaces into readable urls for twitch :D
    fixedGame = requests.get(url=api_link, params=parse)
    # Reading the twitch API in json
    data = json.loads(fixedGame.content.decode("utf-8"))
    r, sub = reddit_Setup(subreddit)
    newStreams = new_streamsDef(data)   
    post_toReddit(sub, newStreams)

# Now this is the option from the beginning. Will the script actually do anything or not?
if retrieveLive.lower() == "true":
    retrieveList()
else:
    pass

