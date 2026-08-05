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
        mean TEXT,
        source TEXT,
        sentence TEXT,
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
        "SELECT id,word,mean,source,sentence,note FROM words"
    )
    words = cursor.fetchall()
    if request.method == "POST":
        print(111)
        word = request.form.get("word","").strip()
        source = request.form.get("source","").strip()
        sentence = request.form.get("sentence", "").strip()
        if source and not (source.startswith("《") and source.endswith("》")):
            source = f"《{source}》"
        if sentence and not (sentence.startswith("“") and sentence.endswith("”")):
            sentence = f"“{sentence}”"
        mean = request.form.get("mean","").strip()
        note = request.form.get("note","").strip()
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        cursor.execute(
        """
        INSERT INTO words
        (word,mean,source,sentence,note,create_time)
        VALUES(?,?,?,?,?,?)
        """,
        (word,mean,source,sentence,note,create_time)
        )

        conn.commit()
        conn.close()
        return redirect("/")
    
    conn.close()
    return render_template(
        "index.html",
        words=words
    )

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = sqlite3.connect("words.db")
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM words WHERE id=?",
        (id,)
    )
    conn.commit()
    conn.close()
    return "ok"

init_db()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)