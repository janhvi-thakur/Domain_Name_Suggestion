from flask import Flask, render_template, request
from name_generator import generate_names_llm

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    names = []

    if request.method == "POST":
        url = request.form.get("url", "").strip()
        description = request.form.get("description", "").strip()

        # LLM generation directly from description (+ optional url context)
        names = generate_names_llm(url=url, description=description)

        print("URL:", url)
        print("Description:", description)
        print("Generated names:", names)

    return render_template("index.html", names=names)

if __name__ == "__main__":
    app.run(debug=True)
