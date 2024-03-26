import sqlite3
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# лемматизация и семант парсинг в перспективе после нее в итоге не используется
texts = []
db_conn = sqlite3.connect('girlies.db')
cur = db_conn.cursor()
cur.execute("SELECT songs.song_name, songs.song_lyrics, songs.release_date, songs.genius_link, artists.name "
            "FROM songs "
            "JOIN artists ON songs.artist_id = artists.artist_id")

all = cur.fetchall()
lyrica = all
for n in lyrica:
    a = n[1].split('\n')[1:]
    b = ['⠀' + a[i] for i in range(len(a))]
    r_lyrics = '\n' + '⠀[Verse 1]\n' + '\n'.join(b)
    texts.append(r_lyrics)

with open('lemm.txt', 'w', encoding='utf-8') as text:
    print(texts, file=text)

lemmatizer = WordNetLemmatizer()  # лемматизируем тексты через модель нлтк
lemmatized_t = []
for i in texts:
    lemmatized_w = [lemmatizer.lemmatize(word) for word in word_tokenize(i)]
    lemmatized_w = ' '.join(lemmatized_w)  # сохраняем леммы в один текст для каждой песни
    lemmatized_t.append(lemmatized_w)
text_index = None
closest_sim = 0
word = ''
for idx, text in enumerate(lemmatized_t):
    if word in text:
        text_index = idx
        break

if text_index is not None:
    print(f"текст с словом, наиболее семантически близким к '{word}':")
    print(texts[text_index])
else:
    print(f"ни один из текстов не содержит слово, наиболее семантически близкое к '{word}'")
with open('lemm.txt', 'w', encoding='utf-8') as t:
    print(lemmatized_t, file=t)
