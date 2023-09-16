from flask import Flask, render_template, request
import os
from dotenv import dotenv_values
import openai
import requests
from time import sleep

app = Flask(__name__)


def chat(msgs):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=msgs
    )
    message = response['choices'][0]['message']
    print(message)
    return message


def fetch_news(symbol, key):
    records = []
    headers = {
        'x-api-key': key,
    }
    params = {
        'q': symbol,
        'topic': 'finance',
        'countries': 'US',
        'lang': 'en',
        'from_rank': 0,
        'to_rank': 100,
        'sort_by': 'date',
        'page_size': 5,
        # 'to': '1 day ago'
    }

    r = requests.get('https://api.newscatcherapi.com/v2/search', params=params, headers=headers)
    data = r.json()
    # data = {
    #     "status": "ok",
    #     "total_hits": 7471,
    #     "page": 1,
    #     "total_pages": 7471,
    #     "page_size": 1,
    #     "articles": [
    #         {
    #             "title": "Is an Apple Music Subscription Worth It?",
    #             "author": "Shujaa Imran",
    #             "published_date": "2022-02-03 16:53:12",
    #             "published_date_precision": "full",
    #             "link": "https://www.makeuseof.com/apple-music-subscription-worth-it",
    #             "clean_url": "makeuseof.com",
    #             "excerpt": "Thinking of subscribing to Apple Music? Here's how to know if it's worth it for you.",
    #             "summary": "Since its launch in June 2015, Apple Music has been growing steadily. Because of its easy integration across Apple devices, many Apple users are fond of the streaming service. However, how does Apple Music stack up compared to the other streaming services out there? Does it justify a $9.99 subscription per month? We'll break down all the details for you, so you can decide whether an Apple Music subscription is truly worth it. What Is Apple Music?\nApple Music is the Apple's music streaming service, which allows subscribers to access millions of content for a subscription fee. With over 90 million songs, Apple Music content can either be streamed online or downloaded to your device for offline listening. \n\nConsidering Apple was late to the streaming market, its music streaming service has performed well. While Apple hasn't released any official figures, reports say that Apple Music had over 523 million subscribers by the end of 2021.\nAccording to Midia Research, Apple Music achieved a market share of 15% in 2021. In comparison, Spotify came at first place and captured 31% of the global streaming market in the same year. An Apple Music subscription combines subscription-based music streaming with global radio-like programming. With this, purchasing a subscription doesn't just unlock Apple Music's extensive 90-million song library for you to use. Apple Music also lets you watch music videos without ads, access a few podcasts, listen to its curated playlists, and tune into Apple Music's radio stations.\nApple's main radio offering, Apple Music 1, features an around-the-clock worldwide live broadcast from DJs based in Los Angeles, New York, and London. Other radio stations include Apple Music Hits, which play everyone's favorite songs from the '80s, '90s, and 2000s, and Apple Music Country, which features country music. Which Devices Does Apple Music Work on?\nApple Music is primarily available in the Music app on all iPhones, iPads, and iPod Touch models running iOS 8.4 or later. Aside from this, Apple Music is also available on PC (iTunes app), Mac (Music app), Apple TV, and Apple Watch. Apple Music is also available on non-Apple devices, such as Android phones, smart TVs, streaming boxes, and even game consoles. Alternatively, you can also access Apple Music online at music.apple.com.\nWhen using Apple Music, you can choose to either stream everything directly from the internet or download it onto your device for offline listening. If you're concerned about data usage, or you'll mostly be in an area without a good wireless connection, offline listening is a great feature. However, it could be an issue if you're already running low on storage space on your device.\nSimilar to other streaming services, you don't own the music files downloaded from Apple Music. With this, you won't be able to offload them anywhere else, burn them onto a disk, or use them in separate video projects. So, if you decide to cancel your Apple Music subscription, you'll lose access to your library. The Benefits of Apple Music\nApple Music works across different platforms including Android. However, its primary advantage is that it's integrated into Apple's ecosystem—meaning you can easily listen to your collection on your iPhone, iPad, Mac, and even Apple Watch.\nIn addition, Apple Music also features high-quality audio playback for audiophiles. For those who enjoy quality streaming, Apple Music offers Lossless, Hi-Res Lossless, Dolby Atmos, and Spatial Audio content, which arrived in June 2021.\nApart from your personal music library, Apple Music can help you enhance your collection with a mix of old and new tracks, along with Apple Music's three live radio stations. You can also stream TV shows, podcasts, music videos, and over 30,000 expertly curated playlists. The Drawbacks of Apple Music\nApple Music's main competitor, Spotify, also offers a robust streaming experience. A key drawback of Apple Music is that it doesn't offer a free version, whereas Spotify does, albeit with ads. Comparatively, Spotify also has a more extensive library than Apple Music, and offers better social media integration. Although, Apple Music still has better integration with the Apple ecosystem, and its content library is increasing every day.\nWhile Apple Music also includes podcasts, they're few and far in between. So, if you're looking for a way to listen to podcasts, Apple Podcasts has a much bigger and organized library. How Much Does Apple Music Cost?\nDepending on your needs, Apple Music operates as a subscription-based service and has different plans available. The basic monthly subscription is $10, which is the same as Spotify Premium and Tidal HiFi.\nAlternatively, you can pay an annual fee of $99. Other plans include a student subscription for $5 per month and a family plan that can be shared between six people for $15 per month. Apple also offers the Apple Music Voice Plan, which is available for $5 per month. The catch—you can only use Siri to verbally request songs, and the service is streaming only. With Apple Music Voice Plan, you can't use the app, download songs, use the Lyrics view, or access Apple's full Lossless audio and Dolby Atmos catalog. Does Apple Music Offer a Free Trial?\nUsually, Apple Music offers a 3-month trial for users looking to try out the subscription, after which it reverts to $9.99 per month. However, while there is no way to use Apple Music for free forever, there are a ton of ways to get it free for longer.\nWith free trials, you can choose to try out the service before you commit to a subscription. If you're not sold on Apple Music, you can simply cancel the trial before it expires. Gone are the times of playing music using CDs—digital music streaming is the new thing. While there are multiple streaming services to pick from, there's no doubt that Apple Music is worth considering.\nIf you own an Apple device, and you're actively looking to get a subscription for your music needs, we'd recommend giving Apple Music a try. In true Apple fashion, Apple Music makes things much easier for a variety of reasons. However, once you get tied into the ecosystem, it can become difficult to escape from. \n How to Get Started Using Apple Music Playlists In this article, we explore how to create, populate, share, discover, and become a master of Apple Music playlists. Related Topics Entertainment IPhone Media Streaming Apple Apple Music \n About The Author Shujaa Imran (54 Articles Published) More From Shujaa Imran Join our newsletter for tech tips, reviews, free ebooks, and exclusive deals!",
    #             "rights": "makeuseof.com",
    #             "rank": 1729,
    #             "topic": "news",
    #             "country": "CA",
    #             "language": "en",
    #             "authors": [
    #                 "Shujaa Imran"
    #             ],
    #             "media": "https://static1.makeuseofimages.com/wordpress/wp-content/uploads/2022/02/thomas-kolnowski-uY-9Dyz8PPM-unsplash-2-1.jpg",
    #             "is_opinion": False,
    #             "twitter_account": "@MUO_official",
    #             "_score": 11.035287,
    #             "_id": "1017cfad154df78ba22b6b358d672e1f"
    #         }
    #     ],
    #     "user_input": {
    #         "q": "Apple",
    #         "search_in": [
    #             "title_summary"
    #         ],
    #         "lang": None,
    #         "not_lang": None,
    #         "countries": [
    #             "CA"
    #         ],
    #         "not_countries": None,
    #         "from": "2021-12-15 00:00:00",
    #         "to": None,
    #         "ranked_only": "True",
    #         "from_rank": None,
    #         "to_rank": None,
    #         "sort_by": "relevancy",
    #         "page": 1,
    #         "size": 1,
    #         "sources": None,
    #         "not_sources": None,
    #         "topic": None,
    #         "published_date_precision": None
    #     }
    # }
    # print(data)
    if 'articles' in data:
        articles = data['articles']
        for article in articles:
            records.append({'title': article['title'], 'summary': article['summary']})

    return {'symbol': symbol, 'articles': records}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    NEWSCATCHER_API = os.environ.get('NEWSCATCHER_API')
    symbol = request.form['symbol'].upper()
    message_history = []
    sentiments = []
    openai.api_key = OPENAI_API_KEY
    system_message = 'You will work as a Sentiment Analysis for Financial news. I will share news headline and summary. You will only answer as:\n\n BEARISH,BULLISH,NEUTRAL. No further explanation. \n Got it?'
    message_history.append({'content': system_message, 'role': 'user'})
    response = chat(message_history)
    articles = fetch_news(symbol, NEWSCATCHER_API)['articles']
    for article in articles:
        user_message = '{}\n{}'.format(article['title'], article['summary'])
        message_history.append({'content': user_message, 'role': 'user'})
        response = chat(message_history)
        sentiments.append(
            {'title': article['title'], 'summary': article['summary'], 'signal': response['content'].replace('.', '')})
        message_history.pop()
        sleep(1)
    # Render the HTML template with the search results
    return render_template('index.html', data=sentiments, query=symbol)


if __name__ == '__main__':
    config = dotenv_values(".env")
    NEWSCATCHER_API = config['NEWSCATCHER_API']
    OPENAI_API_KEY = config['OPENAI_API_KEY']
    app.run(debug=True)
