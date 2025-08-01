import os
import requests
from dotenv import load_dotenv
from urllib.parse import urljoin
from typing import Optional, Dict, Any, Union

from .models import Photo, Video, Collection
from .utils import (
    parse_photo,
    parse_video,
    parse_collection
)

load_dotenv()


class PexelsAPIError(Exception):
    """Custom exception for Pexels API errors"""
    pass


class Pexels:
    """A Python wrapper for the Pexels API to easily search and download photos and videos."""

    BASE_URL = "https://api.pexels.com/v1/"
    VIDEO_BASE_URL = "https://api.pexels.com/videos/"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("PEXELS_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required. Provide it directly or set PEXELS_API_KEY environment variable.")
        
        self.headers = {
            "Authorization": self.api_key,
            "User-Agent": "pypexel/0.1.1"
        }


    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None, base_url: Optional[str] = None) -> Dict[str, Any]:
        """Make a requset to the Pexels API.

        Args:
            endpoint (str): The API endpoint
            params (Optional[Dict[str, Any]], optional): Query parameters
            base_url (Optional[str], optional): Base URL to use. Defaults to BASE_URL

        Returns:
            Dict[str, Any]: JSON response from the API

        Raises:
            PexelsAPIError: If the API request fails
        """
        url = urljoin(base_url or self.BASE_URL, endpoint.lstrip('/'))

        # remove `None` values from params
        if params:
            params = { k: v for k, v in params.items() if v is not None }

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                raise PexelsAPIError("API rate limit exceeded. Please wait before making more requests.")
            elif response.status_code == 403:
                raise PexelsAPIError("Invalid API key or insufficient permissions.")
            else:
                raise PexelsAPIError(f"HTTP error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            raise PexelsAPIError(f"Request failed: {str(e)}")
        except ValueError as e:
            raise PexelsAPIError(f"Invalid JSON response: {str(e)}")


    def search_photos(
            self,
            query: str,
            orientation: str = None,
            size: str = None,
            color: str = None,
            locale: str = None,
            page: Optional[int] = 1,
            per_page: Optional[int] = 15,
            as_objects: Optional[bool] = False
        ) -> dict:
        """Search for photos on Pexels

        Args:
            query (str): The search query (e.g., `Ocean`, `Tigers`, `People`)
            orientation (str, optional): Desired photo orientation: `landscape`, `portrait`, or `square`
            size (str, optional): Minimum photo size: `large` (24MP), `medium` (12MP), or `small` (4MP)
            color (str, optional): Desired photo color: `red`, `orange`, `yellow`, `green`, `turquoise`, `blue`, `violet`, `pink`, `brown`, `black`, `gray`, `white`, or hex code
            locale (str, optional): Search locale (e.g., `en-US`, `pt-BR`)
            page (int, optional): Page number (default: `1`)
            per_page (int, optional): Results per page, max `80` (default: `15`)
            as_objects (bool, optional): Return Photo objects instead of raw dict (default: `False`)

        Returns:
            dict: API response containing photos and metadata

        Raises:
            PexelsAPIError: If the API request fails
            ValueError: If parameters are invalid
        """

        if not query:
            raise ValueError("Query parameter is required")
        
        if per_page > 80:
            raise ValueError("per_page cannot exceed 80")
        
        if page < 1:
            raise ValueError("page must be >= 1")

        params = {
            "query": query,
            "orientation": orientation,
            "size": size,
            "color": color,
            "locale": locale,
            "page": page,
            "per_page": per_page,
        }
        
        response = self._make_request("search", params)

        if as_objects:
            return [parse_photo(photo) for photo in response.get('photos', [])]

        return response

    def search_videos(
        self,
        query: str,
        orientation: Optional[str] = None,
        size: Optional[str] = None,
        locale: Optional[str] = None,
        page: Optional[int] = 1,
        per_page: Optional[int] = 15,
        as_objects: Optional[bool] = False
    ) -> Dict[str, Any]:
        """Search for videos on Pexels

        Args:
            query (str): The search query (e.g., `Ocean`, `Tigers`, `People`)
            orientation (str, optional): Desired photo orientation: `landscape`, `portrait`, or `square`
            size (str, optional): Minimum photo size: `large` (4K), `medium` (Full HD), or `small` (HD)
            locale (str, optional): Search locale (e.g., `en-US`, `pt-BR`)
            page (int, optional): Page number (default: `1`)
            per_page (int, optional): Results per page, max `80` (default: `15`)
            as_objects (bool, optional): Return Video objects instead of raw dict (default: `False`)

        Returns:
            dict: API response containing videos and metadata

        Raises:
            PexelsAPIError: If the API request fails
            ValueError: If parameters are invalid
        """
        if not query:
            raise ValueError("Query parameter is required")
        
        if per_page > 80:
            raise ValueError("per_page cannot exceed 80")
        
        if page < 1:
            raise ValueError("page must be >= 1")

        params = {
            "query": query,
            "orientation": orientation,
            "size": size,
            "locale": locale,
            "page": page,
            "per_page": per_page,
        }

        response = self._make_request("search", params, self.VIDEO_BASE_URL)

        if as_objects:
            return [parse_video(video) for video in response.get('videos', [])]
        
        return response


    def get_photo(self, photo_id: Union[int, str], as_object: Optional[bool] = False) -> Dict[str, Any]:
        """Get a specific photo by ID.

        Args:
            photo_id (int or str): The photo ID
            as_object (bool, optional): Return Photo object instead of raw dict (default: `False`)

        Returns:
            dict: Photo data

        Raises:
            PexelsAPIError: If the API request fails
            ValueError: If parameters are invalid
        """

        response = self._make_request(f"photos/{photo_id}")
    
        if as_object:
            return parse_photo(response)
        
        return response


    def get_video(self, video_id: Union[int, str], as_object: Optional[bool] = False) -> Dict[str, Any]:
        """Get a specific video by ID.

        Args:
            video_id (int or str): The video ID
            as_object (bool, optional): Return Video object instead of raw dict (default: `False`)

        Returns:
            dict: Video data

        Raises:
            PexelsAPIError: If the API request fails
            ValueError: If parameters are invalid
        """

        response = self._make_request(f"videos/{video_id}", base_url=self.VIDEO_BASE_URL)
    
        if as_object:
            return parse_video(response)
        
        return response
    

    def get_curated_photos(
        self,
        page: Optional[int] = 1,
        per_page: Optional[int] = 15,
        as_objects: Optional[bool] = False
    ) -> Dict[str, Any]:
        """Get photos curated by the Pexels team.
        
        Args:
            page (int, optional): Page number (default: `1`)
            per_page (int, optional): Results per page, max `80` (default: `15`)
            as_objects (bool, optional): Return Photo objects instead of raw dict (default: `False`)

        Returns:
            dict: API response containing videos and metadata

        Raises:
            PexelsAPIError: If the API request fails
            ValueError: If parameters are invalid
        """
        
        if per_page > 80:
            raise ValueError("per_page cannot exceed 80")
        
        if page < 1:
            raise ValueError("page must be >= 1")
        
        params = {
            "page": page,
            "per_page": per_page,
        }

        response = self._make_request("curated", params)
    
        if as_objects:
            return [parse_photo(photo) for photo in response.get('photos', [])]

        return response
    

    def get_popular_videos(
        self,
        min_width: Optional[int] = None,
        min_height: Optional[int] = None,
        min_duration: Optional[int] = None,
        max_duration: Optional[int] = None,
        page: Optional[int] = 1,
        per_page: Optional[int] = 15,
        as_objects: Optional[bool] = False
    ) -> Dict[str, Any]:
        """Get the current popular Pexels videos.

        Args:
            min_width (_type_): The minimum width in pixels of the returned videos.
            min_height (_type_): The minimum height in pixels of the returned videos.
            min_duration (_type_): The minimum duration in seconds of the returned videos.
            max_duration (_type_): The maximum duration in seconds of the returned videos.
            page (int, optional): Page number (default: `1`)
            per_page (int, optional): Results per page, max `80` (default: `15`)
            as_objects (bool, optional): Return Video objects instead of raw dict (default: `False`)

        Returns:
            dict: API response containing videos and metadata

        Raises:
            PexelsAPIError: If the API request fails
            ValueError: If parameters are invalid
        """
        
        if per_page > 80:
            raise ValueError("per_page cannot exceed 80")
        
        if page < 1:
            raise ValueError("page must be >= 1")
        
        params = {
            "min_width": min_width,
            "min_height": min_height,
            "min_duration": min_duration,
            "max_duration": max_duration,
            "page": page,
            "per_page": per_page,
        }

        response = self._make_request("popular", params, base_url=self.VIDEO_BASE_URL)
    
        if as_objects:
            return [parse_video(video) for video in response.get('videos', [])]
        
        return response


    def get_featured_collections(
        self,
        page: Optional[int] = 1,
        per_page: Optional[int] = 15,
        as_objects: Optional[bool] = False
    ) -> Dict[str, Any]:
        """Get all featured collections on Pexels

        Args:
            page (int, optional): Page number (default: `1`)
            per_page (int, optional): Results per page, max `80` (default: `15`)
            as_objects (bool, optional): Return Collection objects instead of raw dict (default: `False`)

        Returns:
            dict: API response containing videos and metadata

        Raises:
            PexelsAPIError: If the API request fails
            ValueError: If parameters are invalid
        """        
        
        if per_page > 80:
            raise ValueError("per_page cannot exceed 80")
        
        if page < 1:
            raise ValueError("page must be >= 1")
        
        params = {
            "page": page,
            "per_page": per_page,
        }

        response = self._make_request("collections/featured", params)

        if as_objects:
            return [parse_collection(collection) for collection in response.get('collections', [])]
        
        return response
    
    
    def get_my_collections(
        self,
        page: Optional[int] = 1,
        per_page: Optional[int] = 15,
        as_objects: Optional[bool] = False
    ) -> Dict[str, Any]:
        """Get all of your collections.

        Args:
            page (int, optional): Page number (default: `1`)
            per_page (int, optional): Results per page, max `80` (default: `15`)
            as_objects (bool, optional): Return Collection objects instead of raw dict (default: `False`)

        Returns:
            dict: API response containing videos and metadata

        Raises:
            PexelsAPIError: If the API request fails
            ValueError: If parameters are invalid
        """
        
        if per_page > 80:
            raise ValueError("per_page cannot exceed 80")
        
        if page < 1:
            raise ValueError("page must be >= 1")
        
        params = {
            "page": page,
            "per_page": per_page,
        }

        resposne = self._make_request("collections", params)
    
        if as_objects:
            return [parse_collection(collection) for collection in resposne.get('collections', [])]
        
        return resposne


    def get_collection_media(
        self,
        collection_id: Union[int, str],
        media_type: Optional[str] = None,
        sort: Optional[str] = "asc",
        page: Optional[int] = 1,
        per_page: Optional[int] = 15,
        as_objects: Optional[bool] = False
    ) -> Dict[str, Any]:
        """Get all media within a collection

        Args:
            collection_id (int or str): ID of the Collection
            media_type (str, optional): The type of media you are requesting: `photos` or `videos`. If not given, all media will be returned.
            sort (str, optional): The order of items in the media collection: `asc` or `desc`
            page (int, optional): Page number (default: `1`)
            per_page (int, optional): Results per page, max `80` (default: `15`)
            as_objects (bool, optional): Return Photo/Video objects instead of raw dict (default: `False`)

        Returns:
            dict: API response containing videos and metadata

        Raises:
            PexelsAPIError: If the API request fails
            ValueError: If parameters are invalid
        """        

        if per_page > 80:
            raise ValueError("per_page cannot exceed 80")
        
        if page < 1:
            raise ValueError("page must be >= 1")
        
        if media_type not in ['photos', 'videos', None]:
            raise ValueError("media_type must be either `photos` or `videos`")
        
        params = {
            "type": media_type,
            "sort": sort,
            "page": page,
            "per_page": per_page,
        }

        response = self._make_request(f"collections/{collection_id}", params)

        if as_objects:
            videos = [parse_video(video) for video in [m for m in response.get('media', []) if m.get('type', '') == 'Video']]
            pictures = [parse_photo(photo) for photo in [m for m in response.get('media', []) if m.get('type', '') == 'Photo']]
            return videos + pictures
        
        return response
    

    def download_video(self, video: Video, quality: str) -> str:
        """Download a video from a given URL.
        
        Args:
            video (Video): Video object to download
            quality (str): Requested quality: `sd`, `hd`, `uhd`

        Returns:
            str: The filepath of the downloaded video, or None if download failed
        """

        try:
            available_qualities = set([v.quality for v in video.video_files])

            if quality not in available_qualities:
                raise ValueError(f"`{quality}` is not an available quality. Available: {available_qualities}")

            quality_videos = [v for v in video.video_files if v.quality == quality]
            quality_videos.sort(key=lambda v: v.width, reverse=True)
            selected_video = quality_videos[0]

            video_id = video.id

            response = requests.get(selected_video.link, stream=True, timeout=30)
            response.raise_for_status()

            filename = f"{video_id}_{quality}.mp4"

            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return filename

        except Exception as e:
            print(f"Error downloading vide: {str(e)}")
            return None