import logging
import httpx
from bs4 import BeautifulSoup
from typing import Optional

logger = logging.getLogger(__name__)


async def scrape_url_content(url: str) -> Optional[str]:
    """
    Scrape text content from a URL
    """
    try:
        logger.info(f"Scraping content from URL: {url}")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract text from common article containers
            article_selectors = [
                'article',
                '[role="main"]',
                '.article-content',
                '.post-content',
                '.entry-content',
                '.content',
                'main'
            ]
            
            text_content = ""
            for selector in article_selectors:
                article = soup.select_one(selector)
                if article:
                    text_content = article.get_text(separator=' ', strip=True)
                    break
            
            # Fallback to body if no article found
            if not text_content:
                body = soup.find('body')
                if body:
                    text_content = body.get_text(separator=' ', strip=True)
            
            # Clean up the text
            text_content = ' '.join(text_content.split())
            
            if len(text_content) < 50:
                logger.warning(f"Scraped content too short: {len(text_content)} characters")
                return None
            
            logger.info(f"Successfully scraped {len(text_content)} characters from URL")
            return text_content
            
    except httpx.TimeoutException:
        logger.error(f"Timeout while scraping URL: {url}")
        raise ValueError("URL request timed out")
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error while scraping URL: {e.response.status_code}")
        raise ValueError(f"Failed to access URL: HTTP {e.response.status_code}")
    except Exception as e:
        logger.error(f"Error scraping URL {url}: {str(e)}")
        raise ValueError(f"Failed to scrape content from URL: {str(e)}")
