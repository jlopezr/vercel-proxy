from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class VideoMetadata:
	id: str
	title: str
	description: str
	url: str
	thumbnail: str
	keywords: List[str]
	rating: Optional[str] = None
	rating_scheme: Optional[str] = None
	subtitle: Optional[str] = None
	cue_points: Optional[List[datetime]] = None
	sunrise: Optional[datetime] = None
	sunset: Optional[datetime] = None
	pubDate: Optional[datetime] = None

@dataclass
class Movie(VideoMetadata):
	genre: Optional[str] = None
	category: Optional[str] = None

@dataclass
class Series:
	id: str
	title: str
	description: str
	genre: str
	keywords: List[str]
	category: str
	rating: str
	rating_scheme: str
	thumbnail: str
	
@dataclass
class Episode(VideoMetadata):
	season_number: int = 0
	episode_number: int = 0
	series: Optional[Series] = None
	
@dataclass
class Feed:
	title: str
	description: str
	default_genre: str = "news"
	default_category: str = "unknown"