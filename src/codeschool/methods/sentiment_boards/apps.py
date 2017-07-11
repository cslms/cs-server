from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SentimentBoardConfig(AppConfig):
    name = 'codeschool.methods.sentiment_boards'
    verbose_name = _('Sentiment board')
