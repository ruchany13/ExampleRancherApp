from storages.backends.s3 import S3Storage

class StaticStorage(S3Storage):
    """S3 storage for static files (Cloudflare R2).

    Keeps files under the `static/` prefix in the bucket.
    """
    location = "static"
    default_acl = None
    # sensible default cache for static assets
    object_parameters = {"CacheControl": "max-age=86400, must-revalidate"}


class MediaStorage(S3Storage):
    """S3 storage for uploaded media files.

    Keeps files under the `media/` prefix and avoids overwriting by default.
    """
    location = "media"
    default_acl = None
    file_overwrite = False
    object_parameters = {"CacheControl": "max-age=3600, must-revalidate"}
