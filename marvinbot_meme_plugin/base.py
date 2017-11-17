# -*- coding: utf-8 -*-

from marvinbot.utils import localized_date, get_message
from marvinbot.handlers import CommandHandler, CallbackQueryHandler
from marvinbot.plugins import Plugin
from marvinbot.models import User

import logging
import ctypes
import time
import re
import textwrap

from io import BytesIO

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import os
import inspect

log = logging.getLogger(__name__)


class MarvinBotMemePlugin(Plugin):
    def __init__(self):
        super(MarvinBotMemePlugin, self).__init__('marvinbot_meme_plugin')
        self.bot = None
        self.path = os.path.dirname(inspect.getfile(self.__class__))

    def get_default_config(self):
        return {
            'short_name': self.name,
            'enabled': True
        }

    def configure(self, config):
        self.config = config
        pass

    def setup_handlers(self, adapter):
        self.bot = adapter.bot
        self.add_handler(CommandHandler('meme', self.on_meme_command, command_description='Meme Generator')
            .add_argument('--size', help='Font Size, default 62')
            .add_argument('--top', help='Top text')
            .add_argument('--bottom', help='Bottom text')
        )
 
    def setup_schedules(self, adapter):
        pass

    def make_meme(self, image, text, size=62, top=True):
        text = text.upper()

        if size is None:
            size = 62

        shadowcolor = "black"
        fillcolor = "white"
        
        font = ImageFont.truetype("{}/impact.ttf".format(self.path), int(size))
        original = Image.open(image)
        draw = ImageDraw.Draw(original)

        imageW, imageH = original.size
        charW, charH = draw.textsize(text[0], font)
        charW += 10
        max_char = int(imageW / charW)

        text = "\n".join(textwrap.wrap(text, width=max_char))

        textW, textH = draw.multiline_textsize(text, font)

        x = (imageW-textW)/2

        if top:
            y = 0
        else:
            y = imageH - textH - 10

        draw.multiline_text((x-5, y-5), text, font=font, fill=shadowcolor, align='center')
        draw.multiline_text((x+5, y-5), text, font=font, fill=shadowcolor, align='center')
        draw.multiline_text((x-5, y+5), text, font=font, fill=shadowcolor, align='center')
        draw.multiline_text((x+5, y+5), text, font=font, fill=shadowcolor, align='center')

        draw.multiline_text((x,y), text, font=font, fill=fillcolor, align='center')

        img = BytesIO()
        img.seek(0)
        original.save(img, format='PNG')
        return img

    def on_meme_command(self, update, *args, **kwargs):
        message = get_message(update)

        size = kwargs.get('size')
        top = ""
        bottom = ""

        text = " ".join(message.text.split(" ")[1:])

        # Use the force
        text = text.replace("--","—")

        if "—top" not in text or "—bottom" not in text:
            text = re.sub('—\w*\s+\d+', '', text)

        if "—top" in text:
            top_re = re.compile(".*—top\s([ a-zA-Z0-9\._-¡¿!?\(\)\'\"]*)(\s—.*|$)")
            top = top_re.search(text).group(1)

        if "—bottom" in text:
            bottom_re = re.compile(".*—bottom\s([ a-zA-Z0-9\._-¡¿!?\(\)\'\"]*)(\s—.*|$)")
            bottom = bottom_re.search(text).group(1)

        if "—top" not in text and "—bottom" not in text and "/" in text:
            list_text = text.split("/")
            top = list_text[0]
            bottom = list_text[1]

        if message.reply_to_message and message.reply_to_message.photo:
            photo = message.reply_to_message.photo
            file = self.adapter.bot.getFile(file_id=photo[2]['file_id'])
        
            # Download image
            out = BytesIO()
            out.seek(0)
            file.download(out=out)
            out.seek(0)

            # Make meme
            img = BytesIO()
            img.seek(0)

            if top:
                img = self.make_meme(image=out, text=top, size=size)
                img.seek(0)
                if bottom:
                    img = self.make_meme(image=img, text=bottom, size=size, top=False)
            elif bottom and not top:
                img = self.make_meme(image=out, text=bottom, size=size, top=False)
            elif not top and not bottom:
                img = self.make_meme(image=out, text=text, size=size)

            img.seek(0)
            self.adapter.bot.sendPhoto(chat_id=message.chat_id, photo=img) 
        else:
            msg = "❌ errr!!! where is the photo?"
            self.adapter.bot.sendMessage(chat_id=message.chat_id, text=msg)