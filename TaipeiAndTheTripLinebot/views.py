from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
from linebot.models import *
import googlemaps

import os
import re
import json
import random
import logging
import xml.etree.ElementTree as et

from .models import StoryMap

parser = WebhookParser('6b73a01b00830ba83807e631892d2a9f')
line_bot_api = LineBotApi('sl2F+svVrfEYU4yS1zzqS781L9H8GlzXDMf2TVNQwD041A3QUStV+ZcsmehCVlnFYuPsXfPVlNjrPL7FdvuxS0fJnWR1XmD9DaMXejGpM71Tii6ZF5jvKjv3reKt1WEb19kx4szOpE4OacfrOvAAbQdB04t89/1O/w1cDnyilFU=') 
gmaps = googlemaps.Client(key='AIzaSyBdrIBmvw5wzJeL4DDrtR5TGA-QfenWNno')

the_path =  os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'static'), 'files'), 'travellocationCHINESE_edit.xml')
tree = et.ElementTree(file=the_path)
root = tree.getroot()


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                handle_text_message(event)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


# ================= 機器人區塊 Start =================
def handle_text_message(event):                  # default
    msg = event.message.text #message from user
    # 針對使用者各種訊息的回覆 Start =========
    outcome = process(msg)
    print(outcome)
    if outcome is not None and outcome[0] == 1:
        colsimg = list()
        for y in range(0, len(outcome[1]), 1):
            colimg = ImageCarouselColumn(
                image_url=outcome[1][y],
                action=URITemplateAction(
                    label=' ',
                    uri=outcome[1][y]
                )
            )
            colsimg.append(colimg)
        Image_Carousel = TemplateSendMessage(
        alt_text='目錄 template',
        template=ImageCarouselTemplate(
        columns=colsimg
    )
    )
        line_bot_api.reply_message(event.reply_token,Image_Carousel)

    elif outcome is not None and outcome[0] == 2:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='「'+outcome[1]+'」的小故事：\n    '+outcome[2]))

    elif outcome is not None and outcome[0] == 3:
        cols = list()
        for s in range(0, outcome[1], 1):
            col = CarouselColumn(thumbnail_image_url=str(outcome[5][s]),
                title=outcome[2][s],
                text='地址：'+ outcome[3][s],
                actions=[
                    PostbackTemplateAction(
                        label='story',
                        text=str(outcome[4][s]+1)+'story',
                        data=str(outcome[4][s]+1)+'story'
                        ),
                    PostbackTemplateAction(
                        label='photo',
                        text=str(outcome[4][s]+1)+'photo',
                        data=str(outcome[4][s]+1)+'photo'
                        ),
                ]
            )

            cols.append(col)

        Carousel_template = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
        columns=cols
        )
        )
        line_bot_api.reply_message(event.reply_token,Carousel_template)
    elif outcome is not None and outcome[0] == 4:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=outcome[1]))
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='很抱歉，未找到台北市內的相關景點訊息。'))


def process(msg):
    pattern1 = r'[\d]+[photo]'
    pattern2 = r'[\d]+[story]'
    if re.match(pattern1, msg):
        img_bound = list()
        img_bound_l = list()
        storymap_ph = StoryMap.objects.get(RowNumber=msg[: -5])
        img_bound = storymap_ph.fileurl.split(',')

        for a in img_bound:
            if a != None:
                newimgurl = 'https'+a[4: ]
                img_bound_l.append(newimgurl)

        return [1, img_bound_l]

    elif re.match(pattern2, msg):
        storymap_s = StoryMap.objects.get(RowNumber=msg[: -5])
        storytitle = storymap_s.stitle
        storyshow = storymap_s.xbody

        return [2, storytitle, storyshow]

    elif gmaps.geocode(msg):
        geocode_result = gmaps.geocode(msg)
        max_lat = geocode_result[0]['geometry']['location']['lat'] + 0.01
        min_lat = geocode_result[0]['geometry']['location']['lat'] - 0.01
        max_lng = geocode_result[0]['geometry']['location']['lng'] + 0.01
        min_lng = geocode_result[0]['geometry']['location']['lng'] - 0.01

        store_list = list()
        stitle_list = list()
        addr_list = list()
        img_list = list()
        img_list_a = list()

        for i in range(0,len(root),1):
            for child in root[i]:
                if child.tag == "longitude" and child.text != None:
                        if float(child.text) >= min_lng and float(child.text) <= max_lng:
                            store_list.append(i)

                elif child.tag == "latitude" and child.text != None:
                        if float(child.text) < min_lat or float(child.text) > max_lat:
                            if i in store_list:
                                store_list.remove(i)

                else:
                    pass

        if len(store_list) >= 10:
            length = 10
            random.shuffle(store_list)
        elif len(store_list) < 10 and len(store_list) > 0:
            length = len(store_list)
        else:
            return [4, '很抱歉，未找到台北市內的相關景點訊息。']

        for n in range(0,len(store_list),1):
            for child2 in root[store_list[n]]:
                if child2.tag == "stitle":
                    stitle_list.append(child2.text)
                elif child2.tag == "address":
                    if len(child2.text)>60:
                        addresstext = child2.text[0:56]
                    else:
                        addresstext = child2.text
                    addr_list.append(addresstext)
                elif child2.tag == "file":
                    for grandchild in child2:
                        if grandchild.tag == "img":
                            img_list.append(grandchild.text)
                            break

        if len(img_list) != 0:
            for p in img_list:
                newurl = 'https'+p[4:]
                img_list_a.append(newurl)

        return [3, length, stitle_list, addr_list, store_list, img_list_a]


def writein(request):
    StoryMap.objects.all().delete()
    for x in range(0,len(root),1):
        for search in root[x]:
            if search.tag == "RowNumber" and search.text != None:
                RowNumber = search.text
            elif search.tag == "REF_WP" and search.text != None:
                REF_WP = search.text
            elif search.tag == "CAT1" and search.text != None:
                CAT1 = search.text
            elif search.tag == "CAT2" and search.text != None:
                CAT2 = search.text
            elif search.tag == "MEMO_TIME" and search.text != None:
                MEMO_TIME = search.text
            elif search.tag == "SERIAL_NO" and search.text != None:
                SERIAL_NO = search.text
            elif search.tag == "stitle" and search.text != None:
                stitle = search.text
            elif search.tag == "xbody" and search.text != None:
                xbody = search.text
            elif search.tag == "idpt" and search.text != None:
                idpt = search.text
            elif search.tag == "address" and search.text != None:
                address = search.text
            elif search.tag == "file":
                for i, searchild in enumerate(search):
                    if searchild.tag == "img" and searchild.text != None:
                        print(searchild.text)
                        if i == 0:
                            urladd = str(searchild.text)
                        else:
                            urladd = urladd + ',' + str(searchild.text)
            elif search.tag == "info" and search.text != None:
                info = search.text
            elif search.tag == "longitude" and search.text != None:
                longitude = float(search.text)
            elif search.tag == "latitude" and search.text != None:
                latitude = float(search.text)
            elif search.tag == "MRT" and search.text != None:
                MRT = search.text

        StoryMap.objects.create(RowNumber=RowNumber, REF_WP=REF_WP, CAT1=CAT1, CAT2=CAT2, MEMO_TIME=MEMO_TIME, \
            SERIAL_NO=SERIAL_NO, stitle=stitle, xbody=xbody, idpt=idpt, address=address, \
                fileurl=urladd, info=info, longitude=longitude, latitude=latitude, MRT=MRT)

    return HttpResponse("<script>alert('已完成！');location.href='/'</script>")
