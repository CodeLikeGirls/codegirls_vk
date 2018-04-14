#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import vk_api
import re
import csv
from time import time
from datetime import datetime
import pandas as pd

csvname = '*.csv'

login = '+79****'
passw = '****'
vk_session = vk_api.VkApi(login, passw)
vk_session.auth()
vk = vk_session.get_api()


# Получить список id постов 
def days_ids():
    r = vk.wall.get(owner_id='-143646422')
    p_id = []
    for item in r['items']:
        if re.findall(r'#spring2018@days_of_code', item['text']) \
        and re.findall(r'День', item['text']):
            p_id.append(item['id'])
    return p_id 


# Сбор коментариев за день в словарь 
#{'имя фамилия' : [#теги] или текст комментария}
def get_name_comments(post_id):
    get_comments = vk.wall.getComments(owner_id='-143646422', post_id=post_id, \
                                       count=100, extended=1)
    id_text = {}
    for item in get_comments['items']:
        if re.findall(r'\[id\d', item['text']): 
            continue
        tags = re.findall(r'#\w*', item['text'])
        id_text[item['from_id']] = tags if tags else item['text']
    id_name = {}
    for profil in get_comments['profiles']:
        id_name[profil['id']] = '{} {}'.format(profil['first_name'], \
                                               profil['last_name'])
    name_text = {}
    for key in  list(id_text.keys()):
        name_text[id_name[key]] = id_text[key]
    return name_text


# Получить список словарей комментариев за все дни
def list_all_day_comments():
    list_comments = []
    days_list = days_ids()
    days_list.reverse()
    for d in days_list:
        list_comments.append(get_name_comments(d))
    return list_comments


com = list_all_day_comments()

# Записать список словарей в таблицу
df3 = pd.DataFrame(com)
df3.to_csv(csvname, sep=',')
