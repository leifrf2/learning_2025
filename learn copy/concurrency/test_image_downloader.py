import image_downloader
from requests import Response


class Test_ImageDownloader:
    config = image_downloader.ImageDownloaderConifg(
        app_name="test_app",
        application_id="test_app_id",
        access_key="test_access_key",
        rate_limit_h=50,
        secret_key="test_secret_key"
    )

    def test_one(self):
        assert 1 == 1

    def test_config(self):
        assert self.config.app_name == "test_app"

    def test_rate_limit_parse(self):
        resp: Response = Response()
        resp.headers = {
            'X-Ratelimit-Limit' : 50,
            'X-Ratelimit-Remaining': 40,
            'foo' : 10
        }

        rl: image_downloader.RateLimit = image_downloader.get_rate_limits_from_response(resp)
        assert rl.rate_limit_h == 50
        assert rl.rate_limit_remaining_h == 40
            