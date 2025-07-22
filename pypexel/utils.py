from typing import Dict, Any

from .models import (
    Photo,
    PhotoSRC,
    Video,
    VideoFile,
    VideoPicture,
    Collection,
    User
)


def parse_photo(photo_data: Dict[str, Any]) -> Photo:
    """Parse raw photo data into Photo dataclass"""

    src_data = photo_data.get('src', {})
    photo_src = PhotoSRC(
        original=src_data.get('original', ''),
        large=src_data.get('large', ''),
        large2x=src_data.get('large2x', ''),
        medium=src_data.get('medium', ''),
        small=src_data.get('small', ''),
        portrait=src_data.get('portrait', ''),
        landscape=src_data.get('landscape', ''),
        tiny=src_data.get('tiny', '')
    )

    return Photo(
        id=photo_data.get('id', 0),
        width=photo_data.get('width', 0),
        height=photo_data.get('height', 0),
        url=photo_data.get('url', ''),
        photographer=photo_data.get('photographer', ''),
        photographer_url=photo_data.get('photographer_url', ''),
        photographer_id=photo_data.get('photographer_id', 0),
        avg_color=photo_data.get('avg_color', ''),
        src=photo_src,
        alt=photo_data.get('alt', '')
    )


def parse_video(video_data: Dict[str, Any]) -> Video:
    """Parse raw video data into Video dataclass"""

    user_data = video_data.get('user', {})
    user = User(
        id=user_data.get('id', 0),
        name=user_data.get('name', ''),
        url=user_data.get('url', '')
    )

    video_files = []
    for file_data in video_data.get('video_files', []):
        video_file = VideoFile(
            id=file_data.get('id', 0),
            quality=file_data.get('quality', ''),
            file_type=file_data.get('file_type', ''),
            width=file_data.get('width', 0),
            height=file_data.get('height', 0),
            fps=file_data.get('fps', 0.0),
            link=file_data.get('link', '')
        )
        video_files.append(video_file)

    video_pictures = []
    for pic_data in video_data.get('video_pictures', []):
        video_picture = VideoPicture(
            id=pic_data.get('id', 0),
            picture=pic_data.get('picture', ''),
            nr=pic_data.get('nr', 0)
        )
        video_pictures.append(video_picture)

    return Video(
        id=video_data.get('id', 0),
        width=video_data.get('width', 0),
        height=video_data.get('height', 0),
        url=video_data.get('url', ''),
        image=video_data.get('image', ''),
        duration=video_data.get('duration', 0),
        user=user,
        video_files=video_files,
        video_pictures=video_pictures
    )

def parse_collection(collection_data: Dict[str, Any]) -> Collection:
    """Parse raw collection data into Colleciton dataclass"""

    return Collection(
        id=collection_data.get('id', ''),
        title=collection_data.get('title', ''),
        description=collection_data.get('description', ''),
        private=collection_data.get('private', True),
        media_count=collection_data.get('media_count', 0),
        photos_count=collection_data.get('photos_count', 0),
        videos_count=collection_data.get('videos_count', 0)
    )