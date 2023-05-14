import os
import requests
import hashlib
from instaloader import instaloader



class InstaLoader():
    video_url: str | None = None

    def __init__(self, url: str, path: str | None = None) -> None:
        self.loader = instaloader.Instaloader()
        self.url = url 
        if path:
            self.path = path

        if not path:
            self.path = os.path.dirname(__file__)

    def get_video_url(self) -> str | None:

        post = instaloader.Post.from_shortcode(
            self.loader.context, shortcode=self.url.split("/")[-2])

        for node in post.get_sidecar_nodes():
            if node.is_video:
                self.video_url = node.video_url
                return self.video_url

        if post.is_video:
            self.video_url = post.video_url
            return self.video_url

        self.video_url = None
        return None

    def download_video(self, url: str | None = None) -> str:
        if not url:
            url = self.get_video_url()

        response = requests.get(url=url)
        filename = os.path.join(
            self.path,
            self.get_filename(content=response.content)
        )

        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename

    def get_filename(self, content: str):
        video_hash = hashlib.md5(content).hexdigest()
        return f'{video_hash}.mp4'
