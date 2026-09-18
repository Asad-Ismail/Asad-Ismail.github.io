"""Check a built site: python3 scripts/check_site.py /path/to/build."""
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

root = Path(sys.argv[1]).resolve()

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.main_nav = False
        self.nav_links = []
        self.ids = set()
        self.headings = 0
        self.schema = False
        self.schemas = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'nav': self.main_nav = attrs.get('aria-label') == 'Main navigation'
        if tag == 'a' and self.main_nav: self.nav_links.append(attrs.get('href'))
        if tag == 'h1': self.headings += 1
        if 'id' in attrs: self.ids.add(attrs['id'])
        if tag in ('a', 'link', 'img', 'script'):
            value = attrs.get('href') or attrs.get('src')
            if value: self.links.append(value)
        if tag == 'img': assert 'alt' in attrs, 'Image needs alt text'
        self.schema = tag == 'script' and attrs.get('type') == 'application/ld+json'
    def handle_data(self, data):
        if self.schema: self.schemas.append(json.loads(data))
    def handle_endtag(self, tag):
        if tag == 'script': self.schema = False
        if tag == 'nav': self.main_nav = False

pages = {}
for path in root.rglob('*.html'):
    html = path.read_text()
    if 'http-equiv=refresh' in html or 'http-equiv="refresh"' in html: continue
    page = Page()
    page.feed(html)
    assert page.headings == 1, (str(path), page.headings)
    assert {'/posts/', '/content/', '/projects/', '/about/'} <= set(page.nav_links), f'{path}: missing main navigation'
    pages[path] = page
for path, page in pages.items():
    for href in page.links:
        url = urlsplit(href)
        if url.scheme or url.netloc: continue
        target = (root / unquote(url.path).lstrip('/')) if url.path.startswith('/') else path.parent / unquote(url.path)
        if not url.path: target = path
        if target.is_dir(): target /= 'index.html'
        assert target.exists(), f'{path.relative_to(root)}: broken link {href}'
        if url.fragment and target in pages:
            assert unquote(url.fragment) in pages[target].ids, f'Broken fragment {href}'
archive = (root/'posts/index.html').read_text()
expected_posts = sum(1 for p in Path('content/posts').glob('*.md') if p.stem != '_index' and 'draft = true' not in p.read_text())
assert archive.count('class=writing-row') + archive.count('class="writing-row"') == expected_posts
projects = json.loads(Path('data/projects.json').read_text())
project_page = (root/'projects/index.html').read_text()
assert all(project['url'] in project_page for project in projects)
home = pages[root/'index.html']
assert len(home.schemas) == 1
assert {'writing', 'videos', 'projects'} <= home.ids
videos = json.loads(Path('data/videos.json').read_text())
video_links = [f"https://www.youtube.com/watch?v={video['id']}" for video in videos]
assert set(video_links) <= set(pages[root/'content/index.html'].links)
assert set(video_links[:2]) <= set(home.links)
print(f'PASS: {len(pages)} HTML pages, all internal links/assets, heading structure, JSON-LD, {expected_posts} articles, {len(projects)} projects, {len(videos)} videos, main navigation')
