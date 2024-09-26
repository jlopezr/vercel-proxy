import tempfile
import urllib
from rss import get_rss
from rss_reader import read_rss
from videometadata import Feed, Movie

feeds = [
    ("https://newsml.europapress.net/videos.aspx?usrId=bAWeK5SXmH&chnId=2","Sucesos"),
    ("https://newsml.europapress.net/videos.aspx?usrId=bAWeK5SXmH&chnId=3","Deportes"),
    ("https://newsml.europapress.net/videos.aspx?usrId=bAWeK5SXmH&chnId=4","Gente"),
    ("https://newsml.europapress.net/videos.aspx?usrId=bAWeK5SXmH&chnId=5","Cultura"),
    ("https://newsml.europapress.net/videos.aspx?usrId=bAWeK5SXmH&chnId=6","Economia"),
    ("https://newsml.europapress.net/videos.aspx?usrId=bAWeK5SXmH&chnId=7","Politica"),
    ("https://newsml.europapress.net/videos.aspx?usrId=bAWeK5SXmH&chnId=8","Sociedad"),
    ("https://newsml.europapress.net/videos.aspx?usrId=bAWeK5SXmH&chnId=9","Internacional"),
    ("https://newsml.europapress.net/videos.aspx?usrId=bAWeK5SXmH&chnId=10","Tecnologia"),
    ("https://newsml.europapress.net/videos.aspx?usrId=bAWeK5SXmH&chnId=11","Ciencia")
]

def read_feed(feed_url):
    # Download RSS to a temporary file
    try:
        with urllib.request.urlopen(feed_url) as response:
            content = response.read()
            return content
    except urllib.error.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        raise Exception(f"URL error occurred: {e.reason}")

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(response.content)
        tmp_file.flush()
        feed, videos = read_rss(tmp_file.name)
    return feed, videos

def get_merged_feed():
    videos_data = []

    for feed_url, category in feeds:
        feed, videos = read_feed(feed_url)

        # Iterate all videos, prepend "EuropaPress-" to the id and set the category
        for video in videos:          
            # Convert VideoMetadata to Movie to add genre and category
            video = Movie(video.id, video.title, video.description, video.url, video.thumbnail, video.keywords, video.rating, video.rating_scheme, pubDate=video.pubDate)
            video.id = "EuropaPress-" + video.id
            video.category = "EuropaPress"
            video.genre = category
            # Append the video to the list
            videos_data.append(video)

    #     print("Processing feed: " + feed_url)
    #     print("Title: " + feed.title)
    #     print("Description: " + feed.description)
    #     print("Category: " + category)
    #     print("Videos: " + str(len(videos)))
    #     print("Feed: " + str(feed))
    #     print("")

    # print("Total videos: " + str(len(videos_data)))

    feed = Feed("mRSS Europa Press Vídeos", "Europa Press Vídeos")
    feed.default_category = "EuropaPress"

    # write the rss file
    rss = get_rss([], videos_data, feed)

    return rss