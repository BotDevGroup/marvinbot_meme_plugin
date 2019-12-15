import mongoengine
from marvinbot.utils import localized_date

class MemeTemplate(mongoengine.Document):
    chat_id = mongoengine.LongField(required = True)
    user_id = mongoengine.LongField(required = True)
    photo_id = mongoengine.StringField(required = True)

    date_added = mongoengine.DateTimeField(default = localized_date)

    @classmethod
    def by_chatid(cls, chat_id):
        try:
            return cls.objects.get(chat_id = chat_id)
        except cls.DoesNotExist:
            return None
            
    @classmethod
    def by_chatid_photoid(cls, chat_id, photo_id):
        try:
            return cls.objects.get(chat_id = chat_id, photo_id = photo_id)
        except cls.DoesNotExist:
            return None
