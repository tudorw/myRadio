from flask import Flask, render_template, request, send_from_directory
import feedparser
from gpt4all import GPT4All
from datetime import datetime
import argostranslate.package
import argostranslate.translate
import os

from elevenlabs import generate, play, voices
from elevenlabs import set_api_key
from elevenlabs.api.error import APIError

app = Flask(__name__)
set_api_key("4a77fbcdc43fe8f55297d162cc9099a2")

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/audio')
def serve_page():
    return send_from_directory('', 'audio.html')

@app.route('/audiofiles')
def audio_files():
    audio_dir = 'static/audio/'
    mp3_files = [f for f in os.listdir(audio_dir) if f.endswith('.mp3')]
    mp3_files.sort(key=lambda x: os.path.getmtime(os.path.join(audio_dir, x)), reverse=True)
    return {'files': mp3_files}

@app.route('/process', methods=['GET', 'POST'])
def process():
    # nice artwork for voice selections
    # icons for categories
    # implment chosen feed, then retreive all feeds and create master list, consisting of an entry from each feed in rotation , eg feed 1 article 1, feed 2 article 1, feed 3 article 1, feed 1 article 2, feed 2 article 2, etc
    # use voice selection to choose 2 eleven labs voices then alternate between voices
    # insert adverts every X reading
    # allow users to re-broadcast their radio station
    # check attribution requirements, how do we use the platform to encourage publishers to stick with RSS despite losing eyeballs
    # add 'language learner mode' to have native language read then translation
    # group feeds by language, allow you to select spanish to be read in english, etc
    # check and monitor translation quality (allow user feeedback ranking?)
    # calculate cost to generate myRadio stream, hosting + elevenlabs fees
    # monetisation, product placement, advertising, limit rss feed based on subscription, limit time broadcasted to X minutes without sub...
    # play ambient elements in between articles
    # use sound 'hits' like radio jingles, etc, to break up the audio and make it more interesting
    # extend the station metaphor with localised data, local news, weather, traffic reports, etc
    # how to source and monitor quality of rss feeds, check URL exists, validate feed, check feed for 'staleness' and 'spam' or 'off topic'
    # maintain  list of feeds and down vote for html in summary, bad formatting, extraneous code etc
    # machine translation disclaimers, ai summary disclaimers
    # check license terms for used packages, libraries and ancillary data
    # add a minute to the time to cover the encoding gap (simple, complex, count word output and estimate delay, even more complex, sample and update prediction inc time of day, service level data, response times, encoding times)
    # need multilingual assistance in finding and validating relevant rss feed, and judging quality of machine translations and pronunciation
    # expensive, 12000 characters per hour @ 0.18 / 1000 = $2 / hour - 4 hrs a day ~ $8/day * 31 = $240 / month!
    # broadcast, or produce a daily 1/2 hour 'show' and deliver to users, limit of X variations, so no need to re-render audio, just save unique and construct final piece form pre-existing and new elements, 
    # loses 'time' aspect, live aspect, sad face...
    # theme interlude music on country basis

    data = request.get_json()
    to_code = data.get('language')  
    print (to_code)
    from_code =  data.get('feedLanguage')
    print (from_code)
    model = GPT4All("ggml-model-gpt4all-falcon-q4_0.bin")
    

    # Download and install Argos Translate package
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
    filter(
        lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
    ), None
    )
    if package_to_install is not None:
        argostranslate.package.install_from_path(package_to_install.download())
    else:
        print(f"No download required for translation from {from_code} to {to_code}")

    if request.method == 'POST':
        #voice = request.form.get('voice')
        #feed_url = request.form.get('feed')
        #language = request.form.get('language')
        data = request.get_json()  # Get the JSON data sent in the POST request
        
        feedx = data.get('feed')
        
        print(feedx)
        if from_code == "en":
            if feedx == "World News":
                feed = feedparser.parse("http://feeds.bbci.co.uk/news/world/rss.xml")
            if feedx == "Politics":
                feed = feedparser.parse("https://www.theguardian.com/politics/rss")    
            if feedx == "National News":
                feed = feedparser.parse("https://www.independent.co.uk/news/uk/rss")  
            if feedx == "Business":
                feed = feedparser.parse("https://www.telegraph.co.uk/business/rss.xml")  
            if feedx == "Arts & Culture":
                feed = feedparser.parse("https://www.britishcouncil.org/arts/rss")    

        if from_code == "es":
            if feedx == "World News":
                feed = feedparser.parse("https://www.jornada.com.mx/rss/politica.xml")
            if feedx == "Politics":
                feed = feedparser.parse("https://rss.elconfidencial.com/espana/") 
            if feedx == "National News":
                feed = feedparser.parse("https://www.abc.es/rss/feeds/abc_Espana.xml")  
            if feedx == "Business":
                feed = feedparser.parse("https://www.financialred.com/feed/")  
            if feedx == "Arts & Culture":
                feed = feedparser.parse("http://api2.rtve.es/rss/temas_cultura.xml") 

        if from_code == "de":
            if feedx == "World News":
                feed = feedparser.parse("http://www.spiegel.de/schlagzeilen/rss/0,5291,676,00.xml")
            if feedx == "Politics":
                feed = feedparser.parse("https://www.politico.eu/tag/german-politics/feed/")
            if feedx == "National News":
                feed = feedparser.parse("https://newsfeed.zeit.de/index")  
            if feedx == "Business":
                feed = feedparser.parse("https://www.handelsblatt.com/contentexport/feed/top-themen/")  
            if feedx == "Arts & Culture":
                feed = feedparser.parse("https://rss.sueddeutsche.de/rss/Kultur") 

        if from_code == "ru":
            if feedx == "World News":
                feed = feedparser.parse("https://lenta.ru/rss")
            if feedx == "Politics":
                feed = feedparser.parse("https://www.politico.eu/tag/german-politics/feed/")
            if feedx == "National News":
                feed = feedparser.parse("https://ura.news/rss")  
            if feedx == "Business":
                feed = feedparser.parse("https://iz.ru/xml/rss/all.xml")  
            if feedx == "Arts & Culture":
                feed = feedparser.parse("https://tass.com/rss/v2.xml") 
        if from_code == "zh":
            if feedx == "World News":
                feed = feedparser.parse("https://www.scmp.com/rss/91/feed")
            if feedx == "Politics":
                feed = feedparser.parse("https://thediplomat.com/feed/")
            if feedx == "National News":
                feed = feedparser.parse("http://www.chinadaily.com.cn/rss/china_rss.xml")  
            if feedx == "Business":
                feed = feedparser.parse("https://www.chinaeconomicreview.com/feed/")  
            if feedx == "Arts & Culture":
                feed = feedparser.parse("https://thechinaproject.com/feed/")        
        if from_code == "hi":
            if feedx == "World News":
                feed = feedparser.parse("")
            if feedx == "Politics":
                feed = feedparser.parse("")
            if feedx == "National News":
                feed = feedparser.parse("")  
            if feedx == "Business":
                feed = feedparser.parse("")  
            if feedx == "Arts & Culture":
                feed = feedparser.parse("")
        if from_code == "ja":
            if feedx == "World News":
                feed = feedparser.parse("")
            if feedx == "Politics":
                feed = feedparser.parse("")
            if feedx == "National News":
                feed = feedparser.parse("")  
            if feedx == "Business":
                feed = feedparser.parse("")  
            if feedx == "Arts & Culture":
                feed = feedparser.parse("")          

        print (feedx)
        print (feed)


       

        print("Loaded model and rss")
        voice_index = 0
        for entry in feed.entries:
            
            summary_text = entry['summary']
            #print(summary_text)

            
            summary = model.generate(f"Please create a brief summary of the following text: {summary_text}", max_tokens=256, temp=1.1, repeat_penalty=1.18, n_batch=128,top_k=2, top_p=0.1)
            #translated_summary = translate(summary, 'en', language)
            #print (summary)
            
            current_time = datetime.now().strftime("%H:%M")
         
            translated_summary = argostranslate.translate.translate(f"It is {current_time}." + summary, from_code, to_code)
            #print (translated_summary)
     
            if to_code == "en":
                to_code_display="English"
            if to_code == "es":
                to_code_display="Spanish"
            if to_code == "fr":
                to_code_display="French"
            if to_code == "hi":
                to_code_display="Hindi"
            if to_code == "it":
                to_code_display="Italian"
            if to_code == "de":
                to_code_display="German"
            if to_code == "pl":
                to_code_display="Polish"
            if to_code == "pt":
                to_code_display="Portuguese"

            if from_code == "zh":
                from_code_display="China"
            if from_code == "en":
                from_code_display="Britain"                
            if from_code == "de":
                from_code_display="Germany"
            if from_code == "hi":
                from_code_display="India"
            if from_code == "js":
                from_code_display="Japan"
            if from_code == "ru":
                from_code_display="Russia"

            with open('static/title.txt', 'w') as f:
                f.write(f"Language: {to_code_display}\n")
                f.write(f"News Source: {from_code_display}\n")
                f.write(f"{feedx}\n")

            
    
            
           

            
            announcers =  data.get('voices')
 
            if announcers == "voice1":
                voices = ["Rachel"]
            if announcers == "voice2":
                voices = ["Adam", "CYw3kZ02Hs0563khs1Fj", "Elli"]
            if announcers == "voice3":
                voices = ["oWAxZDx7w5VEj9dCyTzz", "ErXwobaYiN019PkySvjV"]
            if announcers == "voice4":
                voices = ["SOYHLrjzK2X1ezoPC6cr", "jsCqWAovK2LkecY7zXl4"]
            voice = voices[voice_index]
            voice_index = (voice_index + 1) % len(voices)

                       
            audio = generate(
            text=translated_summary,
            voice=voice,
            model="eleven_multilingual_v1"
            )
            try:
                with open(f'static/audio/audio_{datetime.now().strftime("%Y%m%d%H%M%S")}.mp3', 'wb') as f:
                    f.write(audio)
            except APIError as e:
                print(f"Error writing audio: {e}")

            # try:
            #     play(audio)
            # except APIError as e:
            #     print(f"Error playing audio: {e}")
            
            # languagelearner = data.get('languagelearner')
            # if languagelearner == "1":
            #     originalaudio = generate(
            #     text=summary,
            #     voice=voice,
            #     model="eleven_multilingual_v1"
            #     )
            #     try:
            #         with open(f'static/audio/audio_{datetime.now().strftime("%Y%m%d%H%M%S")}.mp3', 'wb') as f:
            #             f.write(originalaudio)
            #     except APIError as e:
            #         print(f"Error writing audio: {e}")

                # try:
                #     play(originalaudio)
                # except APIError as e:
                #     print(f"Error playing audio: {e}")  
    return render_template('index.html')

            
       
            
            
@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory('static/audio', filename)
    

if __name__ == "__main__":
    app.run(debug=False)

