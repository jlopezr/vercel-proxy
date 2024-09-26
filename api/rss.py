from lib.europapress_rss import get_merged_feed
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        rss_content = get_merged_feed()
        self.send_response(200)
        self.send_header('Content-Type', 'application/rss+xml')
        self.end_headers()
        self.wfile.write(rss_content.encode('utf-8'))
        return
