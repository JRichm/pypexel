from typing import List
from dataclasses import dataclass

@dataclass
class PhotoSRC:
    original: str
    large: str
    large2x: str
    medium: str
    small: str
    portrait: str
    landscape: str
    tiny: str


@dataclass
class Photo:
    id: int
    width: int
    height: int
    url: str
    photographer: str
    photographer_url: str
    photographer_id: int
    avg_color: str
    src: PhotoSRC
    alt: str


@dataclass
class VideoFile:
    id: int
    quality: str
    file_type: str
    width: int
    height: int
    fps: float
    link: str

@dataclass
class VideoPicture:
    id: int
    picture: str
    nr: int

@dataclass
class User:
    id: int
    name: str
    url: str


@dataclass
class Video:
    id: int
    width: int
    height: int
    url: str
    image: str
    duration: int
    user: User
    video_files: List[VideoFile]
    video_pictures: List[VideoFile]


@dataclass
class Collection:
    id: str
    title: str
    description: str
    private: bool
    media_count: int
    photos_count: int
    videos_count: int