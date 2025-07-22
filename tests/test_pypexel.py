import os
import pytest
import requests
from unittest.mock import patch, Mock

from pypexel.pypexel import Pexels, PexelsAPIError
from pypexel.models import (
    Photo,
    PhotoSRC,
    Video,
    VideoFile,
    VideoPicture,
    User,
    Collection
)
from pypexel.utils import (
    parse_photo,
    parse_video,
    parse_collection
)


class TestPexelsInitialization:
    def test_init_with_api_key(self):
        api_key = "test-key"
        pexels = Pexels(api_key=api_key)
        assert pexels.api_key == api_key
        assert pexels.headers['Authorization'] == api_key
    
    @patch.dict(os.environ, {'PEXELS_API_KEY': "env_api_key"})
    def test_init_with_env_variable(self):
        pexels =  Pexels()
        assert pexels.api_key == "env_api_key"

    @patch.dict(os.environ, {}, clear=True)
    def test_init_without_api_key_raises_error(self):
        with pytest.raises(ValueError, match="API key is required"):
            Pexels()


class TestPexelsAPIRequests:
    @pytest.fixture
    def pexels(self):
        return Pexels(api_key="test-api-key")
    
    @patch('requests.get')
    def test_successful_request(self, mock_get, pexels):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'test', 'data'}
        mock_get.return_value = mock_response

        result = pexels._make_request("test_endpoint")

        assert result == {'test', 'data'}
        mock_get.assert_called_once()


    @patch('requests.get')
    def test_request_with_params(self, mock_get, pexels):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"test": "data"}
        mock_get.return_value = mock_response

        params = {"query": "test", "per_page": 10, "none_value": None}
        pexels._make_request("test_endpoint", params)

        call_args = mock_get.call_args
        assert "none_value" not in call_args[1]["params"]
        assert call_args[1]["params"]["query"] == "test"
        assert call_args[1]["params"]["per_page"] == 10

    
    @patch('requests.get')
    def test_rate_limit_error(self, mock_get, pexels):
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response
        
        with pytest.raises(PexelsAPIError, match="API rate limit exceeded"):
            pexels._make_request("test-endpoint")
    

    @patch('requests.get')
    def test_invalid_api_key_error(self, mock_get, pexels):
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response
        
        with pytest.raises(PexelsAPIError, match="Invalid API key"):
            pexels._make_request("test-endpoint")
    

    @patch('requests.get')
    def test_generic_http_error(self, mock_get, pexels):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response
        
        with pytest.raises(PexelsAPIError, match="HTTP error 500"):
            pexels._make_request("test-endpoint")
    

    @patch('requests.get')
    def test_connection_error(self, mock_get, pexels):
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        with pytest.raises(PexelsAPIError, match="Request failed"):
            pexels._make_request("test-endpoint")


class TestPhotoParsing:
    @pytest.fixture
    def pexels(self):
        return Pexels(api_key="test-api-key")
    

    @pytest.fixture
    def sample_photo_data(self):
        return {
            "id": 12345,
            "width": 1920,
            "height": 1080,
            "url": "https://www.pexels.com/photo/12345/",
            "photographer": "John Doe",
            "photographer_url": "https://www.pexels.com/@johndoe",
            "photographer_id": 123,
            "avg_color": "#2C3E50",
            "alt": "Beautiful landscape",
            "src": {
                "original": "https://example.com/original.jpg",
                "large": "https://example.com/large.jpg",
                "large2x": "https://example.com/large2x.jpg",
                "medium": "https://example.com/medium.jpg",
                "small": "https://example.com/small.jpg",
                "portrait": "https://example.com/portrait.jpg",
                "landscape": "https://example.com/landscape.jpg",
                "tiny": "https://example.com/tiny.jpg"
            }
        }
    

    def test_parse_photo(self, sample_photo_data):
        photo = parse_photo(sample_photo_data)
        
        assert isinstance(photo, Photo)
        assert photo.id == 12345
        assert photo.photographer == "John Doe"
        assert isinstance(photo.src, PhotoSRC)
        assert photo.src.large == "https://example.com/large.jpg"
    

    def test_parse_photo_missing_fields(self):
        """Test photo parsing with missing fields"""
        incomplete_data = {"id": 123}
        photo = parse_photo(incomplete_data)
        
        assert photo.id == 123
        assert photo.photographer == ""
        assert photo.width == 0


class TestVideoParsing:
    @pytest.fixture
    def pexels(self):
        return Pexels(api_key="test-api-key")
    

    @pytest.fixture
    def sample_video_data(self):
        return {
            "id": 54321,
            "width": 1920,
            "height": 1080,
            "url": "https://www.pexels.com/video/54321/",
            "image": "https://example.com/preview.jpg",
            "duration": 30,
            "user": {
                "id": 456,
                "name": "Jane Smith",
                "url": "https://www.pexels.com/@janesmith"
            },
            "video_files": [
                {
                    "id": 1,
                    "quality": "hd",
                    "file_type": "video/mp4",
                    "width": 1920,
                    "height": 1080,
                    "fps": 30.0,
                    "link": "https://example.com/video.mp4"
                }
            ],
            "video_pictures": [
                {
                    "id": 1,
                    "picture": "https://example.com/thumb1.jpg",
                    "nr": 0
                }
            ]
        }
    

    def test_parse_video(self, sample_video_data):
        video = parse_video(sample_video_data)
        
        assert isinstance(video, Video)
        assert video.id == 54321
        assert video.duration == 30
        assert isinstance(video.user, User)
        assert video.user.name == "Jane Smith"
        assert len(video.video_files) == 1
        assert isinstance(video.video_files[0], VideoFile)
        assert video.video_files[0].quality == "hd"


class TestSearchPhotos:
    @pytest.fixture
    def pexels(self):
        return Pexels(api_key="test-api-key")
    

    @pytest.fixture
    def sample_search_response(self):
        return {
            "page": 1,
            "per_page": 15,
            "total_results": 100,
            "next_page": "https://api.pexels.com/v1/search?page=2",
            "photos": [
                {
                    "id": 12345,
                    "photographer": "John Doe",
                    "src": {"large": "https://example.com/large.jpg"},
                    "alt": "Test photo"
                }
            ]
        }
    

    def test_search_photos_validation(self, pexels):
        with pytest.raises(ValueError, match="Query parameter is required"):
            pexels.search_photos("")
        
        with pytest.raises(ValueError, match="per_page cannot exceed 80"):
            pexels.search_photos("test", per_page=100)
        
        with pytest.raises(ValueError, match="page must be >= 1"):
            pexels.search_photos("test", page=0)
    

    @patch.object(Pexels, '_make_request')
    def test_search_photos_raw_response(self, mock_request, pexels, sample_search_response):
        mock_request.return_value = sample_search_response
        
        result = pexels.search_photos("nature")
        
        mock_request.assert_called_once_with("search", {
            "query": "nature",
            "orientation": None,
            "size": None,
            "color": None,
            "locale": None,
            "page": 1,
            "per_page": 15
        })
        
        assert result == sample_search_response
    

    @patch.object(Pexels, '_make_request')
    def test_search_photos_as_objects(self, mock_request, pexels, sample_search_response):
        mock_request.return_value = sample_search_response
        
        result = pexels.search_photos("nature", as_objects=True)
        
        assert len(result) == 1
        assert isinstance(result[0], Photo)
        assert result[0].id == 12345


class TestSearchVideos:    
    @pytest.fixture
    def pexels(self):
        return Pexels(api_key="test-api-key")
    

    @pytest.fixture
    def sample_video_response(self):
        return {
            "page": 1,
            "per_page": 15,
            "total_results": 50,
            "videos": [
                {
                    "id": 54321,
                    "duration": 30,
                    "user": {"name": "Jane Smith"},
                    "video_files": [],
                    "video_pictures": []
                }
            ]
        }
    

    @patch.object(Pexels, '_make_request')
    def test_search_videos_as_objects(self, mock_request, pexels, sample_video_response):
        mock_request.return_value = sample_video_response
        
        result = pexels.search_videos("ocean", as_objects=True)
        
        mock_request.assert_called_once_with("search", {
            "query": "ocean",
            "orientation": None,
            "size": None,
            "locale": None,
            "page": 1,
            "per_page": 15
        }, pexels.VIDEO_BASE_URL)
        
        assert isinstance(result[0], Video)


class TestGetPhotoVideo:    
    @pytest.fixture
    def pexels(self):
        return Pexels(api_key="test-api-key")
    

    @patch.object(Pexels, '_make_request')
    def test_get_photo_raw(self, mock_request, pexels):
        mock_response = {"id": 12345, "photographer": "John Doe"}
        mock_request.return_value = mock_response
        
        result = pexels.get_photo(12345)
        
        mock_request.assert_called_once_with("photos/12345")
        assert result == mock_response
    

    @patch.object(Pexels, '_make_request')
    def test_get_photo_as_object(self, mock_request, pexels):
        mock_response = {
            "id": 12345,
            "photographer": "John Doe",
            "src": {"large": "test.jpg"}
        }
        mock_request.return_value = mock_response
        
        result = pexels.get_photo(12345, as_object=True)
        
        assert isinstance(result, Photo)
        assert result.id == 12345
    

    @patch.object(Pexels, '_make_request')
    def test_get_video_as_object(self, mock_request, pexels):
        mock_response = {
            "id": 54321,
            "user": {"name": "Jane"},
            "video_files": [],
            "video_pictures": []
        }
        mock_request.return_value = mock_response
        
        result = pexels.get_video(54321, as_object=True)
        
        mock_request.assert_called_once_with("videos/54321", base_url=pexels.VIDEO_BASE_URL)
        assert isinstance(result, Video)


class TestCollectionMethods:    
    @pytest.fixture
    def pexels(self):
        return Pexels(api_key="test-api-key")
    

    @pytest.fixture
    def sample_collections_response(self):
        return {
            "collections": [
                {
                    "id": "abc123",
                    "title": "Nature Collection",
                    "description": "Beautiful nature photos",
                    "private": False,
                    "media_count": 50,
                    "photos_count": 45,
                    "videos_count": 5
                }
            ]
        }
    
    @patch.object(Pexels, '_make_request')
    def test_get_featured_collections_as_objects(self, mock_request, pexels, sample_collections_response):
        mock_request.return_value = sample_collections_response
        
        result = pexels.get_featured_collections(as_objects=True)
        
        assert isinstance(result[0], Collection)
        assert result[0].title == "Nature Collection"
    

    @patch.object(Pexels, '_make_request')
    def test_get_collection_media_mixed_types(self, mock_request, pexels):
        mock_response = {
            "media": [
                {
                    "type": "Photo",
                    "id": 1,
                    "src": {"large": "photo.jpg"},
                    "photographer": "John"
                },
                {
                    "type": "Video",
                    "id": 2,
                    "video_files": [],
                    "user": {"name": "Jane"},
                    "video_pictures": []
                }
            ]
        }
        mock_request.return_value = mock_response
        
        result = pexels.get_collection_media("test123", as_objects=True)

        assert len(result) == 2
        assert isinstance(result[0], Video)
        assert isinstance(result[1], Photo)
    
    def test_get_collection_media_validation(self, pexels):
        with pytest.raises(ValueError, match="media_type must be either"):
            pexels.get_collection_media("123", media_type="invalid")


class TestIntegration:
    @pytest.fixture
    def pexels(self):
        return Pexels(api_key="test-api-key")
    

    @patch('requests.get')
    def test_full_photo_search_workflow(self, mock_get, pexels):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "photos": [{
                "id": 12345,
                "photographer": "Test Photographer",
                "src": {"large": "https://example.com/large.jpg"},
                "alt": "Test photo",
                "width": 1920,
                "height": 1080,
                "url": "https://pexels.com/photo/12345",
                "photographer_url": "https://pexels.com/@test",
                "photographer_id": 123,
                "avg_color": "#123456"
            }],
            "page": 1,
            "per_page": 15,
            "total_results": 1
        }
        mock_get.return_value = mock_response
        
        result = pexels.search_photos("test query", as_objects=True)
        
        assert len(result) == 1
        photo = result[0]
        assert isinstance(photo, Photo)
        assert photo.photographer == "Test Photographer"
        assert photo.src.large == "https://example.com/large.jpg"
        
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "query=test+query" in call_args[0][0] or call_args[1]["params"]["query"] == "test query"


@pytest.fixture
def mock_env_clean():
    with patch.dict(os.environ, {}, clear=True):
        yield


@pytest.mark.parametrize("method_name,endpoint", [
    ("get_curated_photos", "curated"),
    ("get_featured_collections", "collections/featured"),
    ("get_my_collections", "collections")
])
def test_pagination_methods(method_name, endpoint):
    pexels = Pexels(api_key="test-key")
    
    with patch.object(pexels, '_make_request') as mock_request:
        mock_request.return_value = {"test": "response"}
        
        method = getattr(pexels, method_name)
        method(page=2, per_page=20)
        
        call_args = mock_request.call_args
        params = call_args[0][1] if len(call_args[0]) > 1 else call_args[1].get('params', {})
        assert params['page'] == 2
        assert params['per_page'] == 20


if __name__ == "__main__":
    pytest.main([__file__, "-v"])