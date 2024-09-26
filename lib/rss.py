from videometadata import Movie, Episode, Feed
from test_data import generate_test_data
from typing import List
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

def defaults(value, default):
    return value if value not in [None, ""] else default

def generate_rss(episodes_list: List[Episode], movies_list: List[Movie], feed: Feed) -> str:

    # Add namespaces to the root element
    namespaces = {
        "amagi": "http://www.amagi.com/rss/namespace",
        "atom": "http://www.w3.org/2005/Atom",
        "dc": "http://purl.org/dc/elements/1.1/",
        "dcterms": "http://purl.org/dc/terms/",
        "media": "http://search.yahoo.com/mrss/"
    }

    # Register namespaces
    for prefix, uri in namespaces.items():
        ET.register_namespace(prefix, uri)

    rss_attributes = {f"xmlns:{k}": v for k, v in namespaces.items()}
    rss = ET.Element("rss", rss_attributes, version="2.0")
    
    title = ET.SubElement(rss, "title")
    title.text = feed.title
    description = ET.SubElement(rss, "description")
    description.text = feed.description
    generator = ET.SubElement(rss, "generator")
    generator.text = "Lovetv Generator"
    lastBuildDate = ET.SubElement(rss, "lastBuildDate")    
    lastBuildDate.text = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")
    language = ET.SubElement(rss, "language")
    language.text = "en"
    version = ET.SubElement(rss, "version")
    version.text = "1.0"

    series = ET.SubElement(rss, "series")
    movies = ET.SubElement(rss, "movies")
    
    # Sort episodes by series, season and episode number
    episodes_list = sorted(episodes_list, key=lambda e: (e.series.title, e.season_number, e.episode_number))

    list_of_series = []
    current_series = None
    for e in episodes_list:
        # print(e.series.title, e.season_number, e.episode_number)
        if current_series != e.series.title:
            current_series = e.series.title
            list_of_series.append([e])
        else:
            list_of_series[-1].append(e)

    # print("-------------------")
    # for s in list_of_series:
    #     print(s[0].series.title)
    #     for e in s:
    #         print(e.season_number, e.episode_number, e.title)

    for s in list_of_series:
        series = ET.SubElement(series, "item")
        series_guid = ET.SubElement(series, "guid")
        series_guid.text = s[0].series.id
        series_title = ET.SubElement(series, "title")
        series_title.text = s[0].series.title
        series_description = ET.SubElement(series, "description")
        series_description.text = s[0].series.description
        series_genre = ET.SubElement(series, "genre")
        series_genre.text = defaults(s[0].series.genre, feed.default_genre)
        series_keywords = ET.SubElement(series, "media:keywords")
        series_keywords.text = ", ".join(s[0].series.keywords)
        series_category = ET.SubElement(series, "media:category")
        series_category.text = defaults(s[0].series.category, feed.default_category)        
        series_rating = ET.SubElement(series, "media:rating")
        series_rating.text = str(s[0].series.rating)
        series_rating.attrib["scheme"] = s[0].series.rating_scheme
        series_thumbnail = ET.SubElement(series, "media:thumbnail")
        series_thumbnail.attrib["url"] = s[0].series.thumbnail

        episodes_list = ET.SubElement(series, "episodes")

        for e in s:
            item = ET.SubElement(episodes_list, "item")
            
            item_guid = ET.SubElement(item, "guid")
            item_guid.text = e.id

            item_title = ET.SubElement(item, "title")
            item_title.text = e.title

            item_description = ET.SubElement(item, "description")
            item_description.text = e.description

            item_episode_number = ET.SubElement(item, "episodeNumber")
            item_episode_number.text = str(e.episode_number)

            item_season_number = ET.SubElement(item, "seasonNumber")
            item_season_number.text = str(e.season_number)

            item_thumbnail = ET.SubElement(item, "media:thumbnail")
            item_thumbnail.attrib["url"] = e.thumbnail

            item_link = ET.SubElement(item, "media:content")
            item_link.attrib["url"] = e.url

            if e.pubDate is not None:
                item_pubDate = ET.SubElement(item, "pubDate")
                item_pubDate.text = movie.pubDate.strftime("%Y-%m-%dT%H:%M:%S+00:00")
        
    for movie in movies_list:
        item = ET.SubElement(movies, "item")

        item_guid = ET.SubElement(item, "guid")
        item_guid.text = movie.id
        
        item_title = ET.SubElement(item, "title")
        item_title.text = movie.title
                
        item_description = ET.SubElement(item, "description")
        item_description.text = movie.description

        item_genre = ET.SubElement(item, "genre")
        if isinstance(movie, Movie):
            item_genre.text = defaults(movie.genre, feed.default_genre)
        else:
            item_genre.text = feed.default_genre

        item_keywords = ET.SubElement(item, "media:keywords")
        item_keywords.text = ", ".join(movie.keywords)

        item_category = ET.SubElement(item, "media:category")
        if isinstance(movie, Movie):
            item_category.text = defaults(movie.category, feed.default_category)
        else:
            item_category.text = feed.default_category

        if movie.rating is not None and movie.rating_scheme is not None:
            item_rating = ET.SubElement(item, "media:rating")
            item_rating.text = movie.rating
            item_rating.attrib["scheme"] = movie.rating_scheme

        item_thumbnail = ET.SubElement(item, "media:thumbnail")
        item_thumbnail.attrib["url"] = movie.thumbnail

        item_content = ET.SubElement(item, "media:content")
        item_content.attrib["url"] = movie.url

        if movie.pubDate is not None:
            item_pubDate = ET.SubElement(item, "pubDate")
            item_pubDate.text = movie.pubDate.strftime("%Y-%m-%dT%H:%M:%S+00:00")
  
    xml_str = ET.tostring(rss, encoding='utf-8', method='xml')
    pretty_xml_as_string = minidom.parseString(xml_str).toprettyxml(indent="    ", encoding='UTF-8').decode('utf-8')
    return pretty_xml_as_string

def write_rss(filename: str, episodes: List[Episode], movies: List[Movie], feed: Feed):
    rss_xml = generate_rss(episodes, movies, feed)
    with open(filename, "w") as file:
        file.write(rss_xml)

if __name__ == "__main__":
    feed = Feed("Test Feed", "A test feed", "news", "TestProvider")
    movies, episodes = generate_test_data()
    write_rss("rss.xml",episodes, movies, feed)