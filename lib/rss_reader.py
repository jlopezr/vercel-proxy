import xml.etree.ElementTree as ET  
from typing import Tuple
from datetime import datetime
from .videometadata import Feed, VideoMetadata

def read_rss(filename) -> Tuple[Feed, VideoMetadata]:
    """
    Reads an RSS file and returns the parsed feed.
    
    :param filename: The path to the RSS file.
    :return: Parsed RSS feed as an ElementTree Element.
    """
    tree = ET.parse(filename)
    return parse_tree(tree)

def read_rss_string(rss_string) -> Tuple[Feed, VideoMetadata]:
    """
    Reads an RSS string and returns the parsed feed.
    
    :param rss_string: The RSS string.
    :return: Parsed RSS feed as an ElementTree Element.
    """
    tree = ET.ElementTree(ET.fromstring(rss_string))
    return parse_tree(tree)

def parse_tree(tree) -> Tuple[Feed, VideoMetadata]:
    root = tree.getroot()

    feed = Feed(
        title=root.find("channel/title").text,
        description=root.find("channel/description").text
    )

    items = root.findall("channel/item")
    videos = []

    for item in items:
        media_content = item.find("media:content", namespaces={"media": "http://search.yahoo.com/mrss/"})

        # Convert pubDate to a datetime object
        pub_date_str = item.find("pubDate").text
        #print("A:"+pub_date_str)
        pub_date = datetime.strptime(pub_date_str, "%Y-%m-%dT%H:%M:%S")
        #print("B:"+str(pub_date))

        video = VideoMetadata(
            id=item.find("guid").text,
            title=item.find("title").text,
            description=item.find("description").text,            
            url=media_content.attrib["url"],
            thumbnail=media_content.find("media:thumbnail", namespaces={"media": "http://search.yahoo.com/mrss/"}).attrib["url"],            
            keywords=item.find("media:keywords", namespaces={"media": "http://search.yahoo.com/mrss/"}).text.split(","),
            #rating=item.find("media:rating", namespaces={"media": "http://search.yahoo.com/mrss/"}).text,
            #rating_scheme=item.find("media:rating", namespaces={"media": "http://search.yahoo.com/mrss/"}).attrib["scheme"],
            #subtitle=item.find("media:subtitle", namespaces={"media": "http://search.yahoo.com/mrss/"}).text
            pubDate=pub_date
        )
        
        videos.append(video)

    return feed, videos

if __name__ == "__main__":
    feed, videos = read_rss("./test_data/europapress-mini.xml")
    print(f"Feed: {feed.title}")
    print(f"Description: {feed.description}")
    for video in videos:
        print("-----------------------------------------")
        print(video)