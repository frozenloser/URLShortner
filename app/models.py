from tortoise.models import Model
from tortoise import fields

class TimestampMixin():
    creationDate = fields.DatetimeField(auto_now_add = True)

class URLShortner(Model, TimestampMixin):
    id = fields.IntField(pk=True)
    url = fields.CharField(255)
    shortUrl = fields.CharField(255)
    status = fields.IntField()
    class Meta:
        table = "url_shortner"
