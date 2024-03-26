import lyricsgenius
from unidecode import unidecode
import time
import json

# подключаемся по api к genius, поставим timeout 10 (по дефолту 5):
genius = lyricsgenius.Genius('BqFzX1DgVLvRDQkxw7CoX4eRsfmgs4ZIQhxqIE4w0Ubn25qfJbn7v0OTbyzeREui', timeout=10)
all = []  # список для сохранения данных о всех песнях в будущей бд


def gracie(name):
    ga = []
    ga_miss = ['Feel Her Interlude', 'If You Only Knew']  # текста этих песен нет (но в метаданных сайта указано,
    # что есть), будем просто игнорировать их
    page = 1
    s = []
    artist = genius.search_artist(name, max_songs=1, sort='title', include_features=True)  # ищем какую-нибудь 1 песню,
    # чтобы получить айди исполнителя
    id = artist.id
    while page:  # зная айди пройдемся по данным всез песен артиста
        request = genius.artist_songs(id,
                                      sort='title',
                                      per_page=50,
                                      page=page)
        time.sleep(1)  # чтобы сайт не отказывал в доступе добавим слип
        s.extend(request['songs'])
        page = request['next_page']
    for n in s:
        a = {}
        if '(' not in n['title'] and n['title'] not in ga_miss and '*' not in n['title']:  # будем игнорировать еще
            # песни с такими символами
            a['artist_id'] = 1
            a['song_name'] = n['title']
            songie = artist.song(n['title'])
            song = songie.lyrics
            song = unidecode(song)  # уберем ненужные символы
            a['song_lyrics'] = song
            a['release_date'] = n['release_date_for_display']
            a['genius_link'] = n['url']
            a['pic'] = n['header_image_url']
            ga.append(a)
    for i in ga:
        if i not in all:
            all.append(i)
    return all


gracie('Gracie Abrams')

# аналогично с другими исполнителями:


def olivia(name):
    ol = []
    ol_miss = []
    page = 1
    s = []
    artist = genius.search_artist(name, max_songs=1, sort='title', include_features=True)
    id = artist.id
    while page:
        request = genius.artist_songs(id,
                                      sort='title',
                                      per_page=50,
                                      page=page)
        time.sleep(1)
        s.extend(request['songs'])
        page = request['next_page']
    for n in s:
        a = {}
        if '(' not in n['title'] and n['title'] not in ol_miss and '*' not in n['title'] and '/' not in n['title'] \
                and 'Setlist' not in n['title'] and '[' not in n['title'] and 'Tour' not in n['title'] \
                and '-' not in n['title']:
            a['artist_id'] = 2
            a['song_name'] = n['title']
            songie = artist.song(n['title'])
            song = songie.lyrics
            song = unidecode(song)
            a['song_lyrics'] = song
            a['release_date'] = n['release_date_for_display']
            a['genius_link'] = n['url']
            a['pic'] = n['header_image_url']
            ol.append(a)
    for i in ol:
        if i not in all:
            all.append(i)
    return all


olivia('Olivia Rodrigo')


def taylor1(name):
    ta1 = []
    ta1_miss = ['All’s Fair In Love And Poetry', 'But Daddy I Love Him', 'Cannon Balls', 'Clara Bow', 'Down Bad',
                'Dear Digdan', 'Family', 'Florida!!!', 'The Tortured Poets Department', 'So Long, London', 'Scream',
                'Who’s Afraid of Little Old Me?',
                'The Smallest Man Who Ever Lived', 'The Alchemy', 'The Albatross', 'The Black Dog', 'The Bolter',
                'Too Beautiful', 'Why is it Even Bitcrushed Lol', 'Fortnight', 'Fresh Out the Slammer', 'Florida!!!', 'Going Louder Folks', 'Guilty as Sin?', 'His Lies',
                'I Can Do It With A Broken Heart', 'I Did Something Bad', 'My Boy Only Breaks His Favorite Toys',
                'Mystified', 'None of the Above']
    page = 1
    s = []
    artist = genius.search_artist(name, max_songs=1, sort='popularity', include_features=True)
    id = artist.id
    while page:
        request = genius.artist_songs(id,
                                      sort='popularity',  # будем сортировать песни по популярности на сайте,
                                      # не алфавиту, как у других исполнительниц
                                      per_page=50,
                                      page=page)
        time.sleep(2)
        s.extend(request['songs'])
        page = request['next_page']
    for n in s[:333]:  # возьмем 333 самые популярные песни тейлор свифт
        a = {}
        if '(' not in n['title'] and n['title'] not in ta1_miss and '[' not in n['title'] and 'Tour' not in n['title'] \
                and '-' not in n['title'] and '*' not in n['title'] and 'Setlist' not in n['title'] \
                and 'Interview' not in n['title'] and '/' not in n['title'] and 'loml' not in n['title'] \
                and 'Speech' not in n['title'] and 'ivy' not in n['title'] and 'Taylor Swift' not in n['title']:
            a['artist_id'] = 3
            a['song_name'] = n['title']
            songie = artist.song(n['title'])
            song = songie.lyrics
            song = unidecode(song)
            a['song_lyrics'] = song
            a['release_date'] = n['release_date_for_display']
            a['genius_link'] = n['url']
            a['pic'] = n['header_image_url']
            ta1.append(a)
    for i in ta1:
        if i not in all:
            all.append(i)
    return all


taylor1('Taylor Swift')

# запишем данные в джисон
with open('data.json', 'w') as file:
    json.dump(all, file)
