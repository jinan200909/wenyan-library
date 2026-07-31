from flask import Flask, render_template, request, redirect
import sqlite3, datetime, random, os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def init_db():
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
    conn = sqlite3.connect(
        os.path.join(BASE_DIR, "words.db")
    )
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # 默认显示全部
    cursor.execute(
        "SELECT id,word,source,mean,note,create_time FROM words"
    )
    words = cursor.fetchall()
    conn.close()
    return render_template(
        "index.html",
        words=words
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

@app.route("/add", methods=["GET", "POST"])
def add():
    conn = sqlite3.connect(
        os.path.join(BASE_DIR, "words.db")
    )
    cursor = conn.cursor()

    if request.method == "POST":
        word = request.form.get("word","").strip()
        source = request.form.get("source","").strip()

        if source and not (source.startswith("《") and source.endswith("》")):
            source = f"《{source}》"
        mean = request.form.get("mean","").strip()
        note = request.form.get("note","").strip()
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
        conn.close()
        return redirect("/")
    
    return render_template("add.html")

@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):

    conn = sqlite3.connect("words.db")

    cursor = conn.cursor()


    if request.method == "POST":

        word = request.form["word"].strip()

        source = request.form["source"].strip()

        if source and not (source.startswith("《") and source.endswith("》")):
            source = f"《{source}》"

        mean = request.form["mean"].strip()

        note = request.form["note"].strip()

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
    app.run(host='0.0.0.0', port=5000, debug=True)