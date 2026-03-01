import re
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

from loguru import logger


# Modern Chrome UA
_DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)

_CLIENT_KWARGS = dict(
    headers={
        "User-Agent": _DEFAULT_UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    },
    verify=False,
    timeout=httpx.Timeout(15, connect=10),
    follow_redirects=True,
    max_redirects=5,
)


def _detect_encoding(response: httpx.Response) -> str:
    """Detect response encoding from headers, BOM, or meta tags."""
    # 1. Explicit charset in Content-Type header
    ct = response.headers.get("content-type", "")
    m = re.search(r"charset=([^\s;]+)", ct, re.I)
    if m:
        return m.group(1).strip('"\'')

    raw = response.content[:4096]

    # 2. BOM detection
    if raw[:3] == b"\xef\xbb\xbf":
        return "utf-8"
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return "utf-16"

    # 3. HTML meta charset tag
    text_snippet = raw.decode("ascii", errors="ignore")
    m = re.search(r'<meta[^>]+charset=["\']?([^"\'\s;>]+)', text_snippet, re.I)
    if m:
        return m.group(1)
    m = re.search(r'<meta[^>]+content=["\'][^"\']*charset=([^"\'\s;]+)', text_snippet, re.I)
    if m:
        return m.group(1)

    # 4. Default: try utf-8, fall back to gb18030 (superset of gbk/gb2312) for Chinese sites
    try:
        response.content.decode("utf-8")
        return "utf-8"
    except (UnicodeDecodeError, ValueError):
        return "gb18030"


def _decode_html(response: httpx.Response) -> str:
    """Decode response content with proper encoding."""
    encoding = _detect_encoding(response)
    try:
        return response.content.decode(encoding, errors="replace")
    except (LookupError, ValueError):
        return response.content.decode("utf-8", errors="replace")


def _extract_title(soup: BeautifulSoup) -> str:
    """Extract page title from multiple sources."""
    # <title> tag
    title_tag = soup.find("title")
    if title_tag and title_tag.string:
        title = title_tag.string.strip()
        # Clean common suffixes like " - 首页" or " | Official Site"
        title = re.split(r"\s*[-|–—]\s*(?:首页|官网|官方网站|Home|Index)\s*$", title, flags=re.I)[0]
        if title:
            return title.strip()

    # og:title
    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        return og["content"].strip()

    # twitter:title
    tw = soup.find("meta", attrs={"name": "twitter:title"})
    if tw and tw.get("content"):
        return tw["content"].strip()

    # h1
    h1 = soup.find("h1")
    if h1 and h1.get_text(strip=True):
        return h1.get_text(strip=True)[:100]

    return ""


def _extract_description(soup: BeautifulSoup) -> str:
    """Extract page description from multiple sources."""
    # Standard meta description (case insensitive)
    for attr in ({"name": "description"}, {"name": "Description"}, {"name": "DESCRIPTION"}):
        tag = soup.find("meta", attrs=attr)
        if tag and (tag.get("content") or tag.get("value")):
            return (tag.get("content") or tag.get("value", "")).strip()

    # og:description
    og = soup.find("meta", property="og:description")
    if og and og.get("content"):
        return og["content"].strip()

    # twitter:description
    tw = soup.find("meta", attrs={"name": "twitter:description"})
    if tw and tw.get("content"):
        return tw["content"].strip()

    return ""


def _extract_icon(soup: BeautifulSoup, base_url: str) -> str:
    """Extract site icon/favicon from multiple sources with priority ordering."""
    candidates = []

    def _has_rel(values, target):
        """Check if rel attribute list contains target."""
        if isinstance(values, list):
            return target in [v.lower() for v in values]
        if isinstance(values, str):
            return target in values.lower()
        return False

    # 1. apple-touch-icon (usually high quality PNG)
    for tag in soup.find_all("link", rel=True):
        rel_val = tag.get("rel", [])
        if _has_rel(rel_val, "apple-touch-icon") or _has_rel(rel_val, "apple-touch-icon-precomposed"):
            href = tag.get("href")
            if href:
                candidates.append(("apple-touch", href))

    # 2. og:image
    og_img = soup.find("meta", property="og:image")
    if og_img and og_img.get("content"):
        candidates.append(("og", og_img["content"]))

    # 3. All <link rel="icon"> variants
    for tag in soup.find_all("link", rel=True):
        rel_val = tag.get("rel", [])
        if not (_has_rel(rel_val, "icon") or _has_rel(rel_val, "shortcut")):
            continue
        href = tag.get("href", "")
        if not href:
            continue
        icon_type = tag.get("type", "")
        sizes = tag.get("sizes", "")

        # SVG icons get high priority
        if "svg" in icon_type.lower() or href.lower().endswith(".svg"):
            candidates.append(("svg", href))
            continue

        # Parse size for sorting (prefer larger)
        size = 0
        m = re.match(r"(\d+)", sizes)
        if m:
            size = int(m.group(1))
        candidates.append((f"icon-{size:05d}", href))

    # Pick the best candidate
    if candidates:
        priority = {"apple-touch": 1, "svg": 2, "og": 5}

        def sort_key(item):
            tag_type, _ = item
            if tag_type.startswith("icon-"):
                size = int(tag_type.split("-")[1])
                return 3, -size  # larger icons rank higher
            return priority.get(tag_type, 7), 0

        candidates.sort(key=sort_key)
        _, best_href = candidates[0]
        return urljoin(base_url, best_href)

    # Fallback: /favicon.ico
    return urljoin(base_url, "/favicon.ico")


async def _fetch_with_retry(url: str, max_retries: int = 2) -> httpx.Response | None:
    """Fetch URL with retry and fallback strategies."""
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            async with httpx.AsyncClient(**_CLIENT_KWARGS) as client:
                response = await client.get(url)
                if response.status_code < 400:
                    return response
                if response.status_code in (403, 429, 503) and attempt < max_retries:
                    last_error = f"HTTP {response.status_code}"
                    continue
                # Even on 4xx/5xx, return it - page might still have useful HTML
                return response
        except httpx.TimeoutException:
            last_error = "timeout"
            logger.warning(f"get_site_info 超时 (attempt {attempt + 1}): {url}")
        except httpx.ConnectError as e:
            last_error = str(e)
            logger.warning(f"get_site_info 连接失败 (attempt {attempt + 1}): {url} - {e}")
        except Exception as e:
            last_error = str(e)
            logger.warning(f"get_site_info 异常 (attempt {attempt + 1}): {url} - {e}")

    # Try https if original was http
    parsed = urlparse(url)
    if parsed.scheme == "http":
        https_url = url.replace("http://", "https://", 1)
        try:
            async with httpx.AsyncClient(**_CLIENT_KWARGS) as client:
                response = await client.get(https_url)
                if response.status_code < 400:
                    return response
        except Exception:
            pass

    logger.error(f"get_site_info 所有尝试失败: {url}, 最后错误: {last_error}")
    return None


async def _validate_icon(icon_url: str, site_url: str) -> str:
    """Validate icon URL is accessible, try fallbacks if not."""
    if not icon_url:
        return ""
    try:
        async with httpx.AsyncClient(**_CLIENT_KWARGS) as client:
            resp = await client.head(icon_url)
            if resp.status_code < 400:
                return icon_url

            # Try common fallbacks
            parsed = urlparse(site_url)
            base = f"{parsed.scheme}://{parsed.netloc}"
            for path in ("/favicon.ico", "/favicon.png", "/logo.png", "/apple-touch-icon.png"):
                try:
                    fb_resp = await client.head(base + path)
                    if fb_resp.status_code < 400:
                        ct = fb_resp.headers.get("content-type", "")
                        if "image" in ct or "icon" in ct or path.endswith(".ico"):
                            return base + path
                except Exception:
                    continue
    except Exception:
        pass

    # Google favicon service as ultimate fallback
    netloc = urlparse(site_url).netloc
    if netloc:
        return f"https://www.google.com/s2/favicons?domain={netloc}&sz=64"
    return icon_url


async def get_site_info(url: str) -> dict | None:
    """
    Fetch site title, icon and description from a URL.

    Improvements:
    - Proper encoding detection (gb2312/gbk/gb18030/utf-8/etc.)
    - Better icon extraction (apple-touch-icon, og:image, SVG, sizes sorting)
    - Better title/description extraction (og:, twitter:, h1 fallback)
    - 15s timeout + 2 retries + https fallback
    - Validates favicon URL accessibility with fallback chain
    - Modern User-Agent (Chrome 131)
    """
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    response = await _fetch_with_retry(url)
    if response is None:
        return None

    # Decode with proper encoding
    html_text = _decode_html(response)
    soup = BeautifulSoup(html_text, "html.parser")

    title = _extract_title(soup)
    desc = _extract_description(soup)
    icon_url = _extract_icon(soup, str(response.url))

    # Validate icon is accessible
    icon_url = await _validate_icon(icon_url, str(response.url))

    result = {
        "title": title or "",
        "icon": icon_url or "",
        "desc": desc or "",
    }

    logger.info(f"get_site_info: {url} -> title={title[:50]!r}" if title else f"get_site_info: {url} -> no title")
    return result


class CdnImg:
    def __init__(self, token, base_url='https://img.ink/api'):
        self.token = token
        self.session = httpx.AsyncClient(
            headers={
                'User-Agent': _DEFAULT_UA,
                'token': self.token
            },
            base_url=base_url,
            verify=False
        )

    async def login(self, username, password):
        resp = await self.session.post('token', data={
            'email': username,
            'password': password
        })
        resp_data = resp.json()
        if resp_data.get('status'):
            self.token = resp_data['data']['token']
            self.session.headers.update({'token': self.token})
            logger.success('登录成功')
            return
        logger.error('登录失败')
        return

    async def get_img_list(self, page: 1, page_size: 20):
        resp = await self.session.post('images', data={
            'page': page,
            'rows': page_size
        })
        if resp.status_code != 200:
            logger.error('获取图片列表失败')
            return
        data = resp.json()
        if data.get('code') == 200:
            logger.success('获取图片列表成功')
            return data.get('data')

    async def upload_img(self, file: str | bytes, filename=''):
        if isinstance(file, str):
            return await self._upload_img_by_url(file, filename)
        elif isinstance(file, bytes):
            return await self._upload_img_by_file(file, filename)

    async def _upload_img_by_url(self, url: str, filename=''):
        filename = filename or url.split('/')[-1]
        async with httpx.AsyncClient(**_CLIENT_KWARGS) as client:
            img_resp = await client.get(url)
        return await self._upload_img_by_file(img_resp.content, filename)

    async def _upload_img_by_file(self, file: bytes, filename=''):
        filename = filename or 'icon.png'
        resp = await self.session.post('upload', files={'image': (filename, file)}, data={
            'folder': 'navicon'
        })
        data = resp.json()
        if data.get('code') == 200:
            logger.success('上传成功')
            return data.get('data')
        raise AttributeError('上传图片失败')

    async def delete_img(self, _id: str):
        await self.session.post('delete', data={
            'id': _id
        })
