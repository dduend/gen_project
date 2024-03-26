from flask import Flask, render_template, request, redirect, url_for
import json
import sqlite3
import random
import matplotlib.pyplot as plt


app = Flask(__name__)

description1 = "здесь вы можете ввести слово и получить текст песни, в котором оно встречается;"
description2 = "⠀если слова нет ни в одной песне, вы получите рандомную лирику"
add = "⠀!! тексты песен тейлор свифт, оливии родриго и грейси абрамс"

# загрузка данных из файла
with open("d.json", "r+") as f:
    datan = json.load(f)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', description1=description1, description2=description2, add=add)
    # в нем используем base.html


@app.route("/questionnaire", methods=['GET', 'POST'])
def quest():
    if request.method == "POST":
        # сохранение введенного слова в список всех со всеми запросами:
        answers = request.form.to_dict()
        datan.append(answers)
        with open("d.json", "w") as h:
            json.dump(datan, h)

        return redirect(url_for("statistics"))
    return render_template('quest.html')


@app.route("/statistics", methods=['GET', 'POST'])
def statistics():
    # работа с поиском по введенному слову
    num_responses = datan[-1]['word']  # введенное сейчас слово - последнее в списке
    db_conn = sqlite3.connect('girlies.db')
    cur = db_conn.cursor()
    cur.execute("SELECT songs.song_name, songs.song_lyrics, songs.release_date, songs.genius_link, artists.name "
                "FROM songs JOIN artists ON songs.artist_id = artists.artist_id "
                "WHERE song_lyrics LIKE '%{0}%';".format(num_responses))

    all = cur.fetchall()

    if len(all) > 0:

        lyrica = random.choice(all)
        cur.close()
        r_name = lyrica[0]

        a = lyrica[1].split('\n')[1:]
        b = ['⠀' + a[i] for i in range(len(a))]

        r_lyrics = '\n' + '⠀[Verse 1]\n' + '\n'.join(b)
        r_date = lyrica[2]
        r_link = lyrica[3]
        r_art = lyrica[4]
        text = 'есть в базе!'
        text2 = ''

    else:
        cur.execute("SELECT songs.song_name, songs.song_lyrics, songs.release_date, songs.genius_link, artists.name "
                    "FROM songs JOIN artists ON songs.artist_id = artists.artist_id".format(num_responses))
        all = cur.fetchall()
        lyrica = random.choice(all)
        r_name = lyrica[0]

        a = lyrica[1].split('\n')[1:]
        b = ['⠀' + a[i] for i in range(len(a))]

        r_lyrics = '\n' + '⠀[Verse 1]\n' + '\n'.join(b)
        r_date = lyrica[2]
        r_link = lyrica[3]
        r_art = lyrica[4]
        text = 'слова нет ни в одном тексте базы :( '
        text2 = ' ⠀исполнительницы используют в лирике другие слова. держите рандомный текст:'
    return render_template("results.html", num_responses=num_responses, r_name=r_name, r_lyrics=r_lyrics, r_date=r_date,
                           r_link=r_link, r_art=r_art, text=text, text2=text2)


@app.route("/data", methods=['GET', 'POST'])
def data():
    with open("d.json", "r+") as f:
        data = json.load(f)
        kol = len(data)  # посчитаем, сколько запросов слов было на нашем сайте
        l = {}
        # посчитаем статистику по длине этих слов:
        for item in data:
            word_length = len(item['word'])
            if word_length in l:
                l[word_length] = l[word_length] + 1
            else:
                l[word_length] = 1
        # построим столбчатую диаграмму
        plt.bar(l.keys(), l.values())
        plt.xlabel('длина слова')  # подпись оси х
        plt.ylabel('частота')  # подпись оси у
        plt.title('частота слов разной длины')  # заголовок
        plt.savefig('static/graph1.png')
        plt.close()

        db_con = sqlite3.connect('girlies.db')
        # посчитаем в базе данных кол-во песен каждого исполнителя
        cur = db_con.cursor()
        cur.execute("SELECT * FROM songs WHERE artist_id = 1")
        all1 = len(cur.fetchall())
        cur = db_con.cursor()
        cur.execute("SELECT * FROM songs WHERE artist_id = 2")
        all2 = len(cur.fetchall())
        cur = db_con.cursor()
        cur.execute("SELECT * FROM songs WHERE artist_id = 3")
        all3 = len(cur.fetchall())

        # посмотрим статистику по годам публикации песен
        curt = db_con.cursor()
        curt.execute("SELECT release_date FROM songs")
        da = {}
        d = curt.fetchall()
        for i in d:
            for m in i:
                m = str(m)
                dataa = str(m.split(', ')[-1])
                if dataa not in da and dataa != 'None':
                    da[dataa] = 1
                elif dataa in da and dataa != 'None':
                    da[dataa] = int(da[dataa]) + 1
        keys = list(da.keys())
        # чтобы график отображался красиво, возьмем 12 рандомных годов
        random_keys = random.sample(keys, 12)
        new_da = {k: da[k] for k in random_keys}
        # сортируем года по порядку по возрастанию
        new_da = dict(sorted(new_da.items(), key=lambda x: x[0]))
        # строим график
        X = list(new_da.keys())
        Y = list(new_da.values())
        plt.plot(X, Y)
        plt.title('частота песен по годам')  # заголовок
        plt.ylabel('количество песен')  # подпись оси Х
        plt.xlabel('год')  # подпись оси Y
        plt.savefig('static/graph2.png')
        plt.close()
    return render_template("data.html", data=data, kol=kol, all1=all1, all2=all2, all3=all3, da=da)


if __name__ == '__main__':
    app.run(debug=True)
