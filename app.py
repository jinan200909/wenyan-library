from flask import Flask, render_template, request, redirect
import sqlite3, datetime, random, os

app = Flask(__name__)


def init_db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    conn = sqlite3.connect(
        os.path.join(BASE_DIR, "words.db")
    )
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS words(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT,
        source TEXT,
        mean TEXT,
        note TEXT,
        create_time TEXT
    )
    """)

    conn.commit()
    conn.close()


@app.route("/", methods=["GET","POST"])
def home():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    conn = sqlite3.connect(
        os.path.join(BASE_DIR, "words.db")
    )
    cursor = conn.cursor()

    if request.method == "POST":

        # 判断是不是添加记录
        if "save" in request.form:

            word = request.form["word"]
            source = request.form["source"].strip()

            if source and not (source.startswith("《") and source.endswith("》")):
                source = f"《{source}》"
            mean = request.form["mean"]
            note = request.form["note"]
            create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


            cursor.execute(
            """
            INSERT INTO words
            (word,source,mean,note,create_time)
            VALUES(?,?,?,?,?)
            """,
            (word,source,mean,note,create_time)
            )

            conn.commit()


        # 判断是不是搜索
        elif "search" in request.form:

            keyword = request.form["keyword"]

            cursor.execute(
            """
            SELECT id,word,source,mean,note,create_time
            FROM words
            WHERE word LIKE ?
            """,
            ('%' + keyword + '%',)
            )

            words = cursor.fetchall()

            conn.close()

            return render_template(
                "index.html",
                words=words
            )


    # 默认显示全部
    cursor.execute(
        "SELECT id,word,source,mean,note,create_time FROM words"
    )

    words = cursor.fetchall()

    cards = []

    for item in words:

        left = random.randint(50, 1000)

        top = random.randint(50, 400)

        rotate = random.randint(-12, 12)


        cards.append(
            (
                item,
                left,
                top,
                rotate
            )
        )

    conn.close()


    return render_template(
        "index.html",
        cards=cards
    )

@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("words.db")

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM words WHERE id=?",
        (id,)
    )

    conn.commit()

    conn.close()

    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):

    conn = sqlite3.connect("words.db")

    cursor = conn.cursor()


    if request.method == "POST":

        word = request.form["word"]

        source = request.form["source"].strip()

        if source and not (source.startswith("《") and source.endswith("》")):
            source = f"《{source}》"

        mean = request.form["mean"]

        note = request.form["note"]

        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        cursor.execute(
        """
        UPDATE words
        SET word=?,
            source=?,
            mean=?,
            note=?,
            create_time=?
        WHERE id=?
        """,
        (word,source,mean,note,create_time,id)
        )


        conn.commit()

        conn.close()


        return redirect("/")


    cursor.execute(
        """
        SELECT word,source,mean,note
        FROM words
        WHERE id=?
        """,
        (id,)
    )


    data = cursor.fetchone()


    conn.close()


    return render_template(
        "edit.html",
        word=data[0],
        source=data[1],
        mean=data[2],
        note=data[3]
    )

if __name__ == "__main__":

    init_db()

    app.run(host='0.0.0.0', port=5000)