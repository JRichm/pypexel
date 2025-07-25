# **pypexel**
A modern, comprehensive Python wrapper for the Pexels API. Search, discover, and download stunning royalty-free photos and videos with ease.

## Features

- **Complete API Coverage** - Search photos, videos, collections, and more
- **Simple Integration** - Just a few lines of code to get started
- **Production Ready** - Robust error handling and rate limit management
- **Type Hints** - Full typing support for better development experience
- **Rich Collections** - Access curated and user collections
- **Video Support** - Search and access Pexels video library
- **Flexible** - Environment variables or direct API key configuration

## Basic Usage
```
from pypexel import Pexels

# Initialize client
pexels = Pexels(api_key="your-api-key-here") # Or use environment variable PEXELS_API_KEY


# Search for photos
photos = pexels.search_photos("mountain landscape", per_page=10)
print(f"Found {photos['total_results']} photos")

# Get photo details
for photo in photos['photos']:
    print(f"📷 {photo['photographer']}: {photo['alt']}")
    print(f"🔗 Download: {photo['src']['large']}")
```

## Documentation
#### Getting Your API key

1.  Sign up at [Pexels](https://www.pexels.com/)   
2.  Go to the [API page](https://www.pexels.com/api/key)   
3.  Generate your free API key   
4.  Set it as an environment variable:

``` PEXELS_API_KEY="your-api-key-here" ```

or pass it directly:   
``` pexels = Pexels(api_key="your-api-key-here") ```


### API Reference

| Method                    | Description               | parameters                                                                    |
|---------------------------|---------------------------|-------------------------------------------------------------------------------|
| search_photos             | Search for photos         | `query`, `orientation`, `size`, `color`, `locale`, `page`, `per_page`         |
| search_videos             | Search for videos         | `query`, `orientation`, `size`, `locale`, `page`, `per_page`                  |
| get_photo                 | Get specific photo        | `photo_id`                                                                    |
| get_video                 | Get specific video        | `video_id`                                                                    |
| get_popular_videos        | Get popular videos        | `min_width`, `min_height`, `min_duration`, `max_duration`, `page`, `per_page` |
| get_curated_photos        | Get curated photos        | `page`, `per_page`                                                            |
| get_featured_collections  | Get featured collections  | `page`, `per_page`                                                            |
| get_my_collections        | Get user collections      | `page`, `per_page`                                                            |
| get_collection_media      | Get collection media      | `collection_id`, `media_type`, `sort`, `page`, `per_page`                     |

###  FAQ
**Is PyPexel free to use?**  
Yes! PyPexel is open source and free. You'll need a free Pexels API key.  
  
**What are the rate limits?**  
Pexels allows 200 requests per hour and 20,000 per month on the free tier. [How do I get unlimited requests?](https://help.pexels.com/hc/en-us/articles/900005852323-How-do-I-get-unlimited-requests)  
  
**Can I use this for commercial projects?**  
Yes, both PyPexel and Pexels content can be used commercially. Check [Pexels License](https://www.pexels.com/license/) for media usage terms.  
  
**How do I get high-resolution images?**  
Use the size="large" parameter and access photo['src']['original'] for the highest resolution.  

## Requirements

• Python 3.7+   
• requests library   
• python-dotenv (optional, for environment variables)   