import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import quote
import time

class URLFetcher:
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'curl/7.68.0',
            'Python-Requests/2.26.0'
        ]

    def _get_session(self):
        """Create a requests session with retry strategy"""
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=(500, 502, 503, 504)
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def fetch(self, url, timeout=10):
        """
        Fetch URL with multiple fallback strategies to bypass 404/403 errors
        
        Args:
            url (str): URL to fetch
            timeout (int): Request timeout in seconds
            
        Returns:
            dict: {
                'success': bool,
                'status_code': int,
                'content': str or None,
                'method': str (strategy used)
            }
        """
        
        # Strategy 1: Direct fetch with various user agents
        for i, user_agent in enumerate(self.user_agents):
            result = self._try_fetch(url, user_agent, timeout)
            if result['success']:
                result['method'] = f'Direct (User-Agent: {i+1})'
                return result
        
        # Strategy 2: Try with Referer header (some sites check this)
        result = self._try_fetch_with_referer(url, timeout)
        if result['success']:
            result['method'] = 'With Referer header'
            return result
        
        # Strategy 3: Try Wayback Machine (archive.org)
        result = self._try_wayback_machine(url, timeout)
        if result['success']:
            result['method'] = 'Wayback Machine Archive'
            return result
        
        # Strategy 4: Try Google Cache
        result = self._try_google_cache(url, timeout)
        if result['success']:
            result['method'] = 'Google Cache'
            return result
        
        # Return last attempt result with failure
        return {
            'success': False,
            'status_code': None,
            'content': None,
            'method': 'All strategies failed',
            'error': 'Unable to fetch URL with any method'
        }

    def _try_fetch(self, url, user_agent, timeout):
        """Try fetching with a specific user agent"""
        try:
            headers = {'User-Agent': user_agent}
            session = self._get_session()
            response = session.get(url, headers=headers, timeout=timeout, allow_redirects=True)
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'status_code': response.status_code,
                    'content': response.text
                }
            elif response.status_code in (404, 403):
                return {
                    'success': False,
                    'status_code': response.status_code,
                    'content': None
                }
        except Exception as e:
            pass
        
        return {'success': False, 'status_code': None, 'content': None}

    def _try_fetch_with_referer(self, url, timeout):
        """Try fetching with Referer header"""
        try:
            headers = {
                'User-Agent': self.user_agents[0],
                'Referer': 'https://www.google.com/'
            }
            session = self._get_session()
            response = session.get(url, headers=headers, timeout=timeout, allow_redirects=True)
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'status_code': response.status_code,
                    'content': response.text
                }
        except Exception as e:
            pass
        
        return {'success': False, 'status_code': None, 'content': None}

    def _try_wayback_machine(self, url, timeout):
        """Try fetching from Wayback Machine (archive.org)"""
        try:
            wayback_url = f'https://archive.org/wayback/available?url={url}&output=json'
            session = self._get_session()
            response = session.get(wayback_url, timeout=timeout)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('archived_snapshots'):
                    snapshot = data['archived_snapshots'].get('closest')
                    if snapshot:
                        archive_url = snapshot.get('url')
                        if archive_url:
                            # Fetch from the archived version
                            archived_response = session.get(archive_url, timeout=timeout)
                            if archived_response.status_code == 200:
                                return {
                                    'success': True,
                                    'status_code': archived_response.status_code,
                                    'content': archived_response.text
                                }
        except Exception as e:
            pass
        
        return {'success': False, 'status_code': None, 'content': None}

    def _try_google_cache(self, url, timeout):
        """Try fetching from Google Cache"""
        try:
            cache_url = f'https://webcache.googleusercontent.com/cache:{url}'
            headers = {'User-Agent': self.user_agents[0]}
            session = self._get_session()
            response = session.get(cache_url, headers=headers, timeout=timeout)
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'status_code': response.status_code,
                    'content': response.text
                }
        except Exception as e:
            pass
        
        return {'success': False, 'status_code': None, 'content': None}


# Convenience function
def fetch_url(url, timeout=10):
    """
    Fetch a URL with automatic fallback strategies
    
    Usage:
        result = fetch_url('https://example.com')
        if result['success']:
            print(f"Fetched using: {result['method']}")
            print(result['content'])
        else:
            print(f"Failed: {result.get('error')}")
    """
    fetcher = URLFetcher()
    return fetcher.fetch(url, timeout)
