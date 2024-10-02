from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portfolio.db"
db = SQLAlchemy(app)

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    portfolios = Portfolio.query.all()
    return render_template("index.html", portfolios=portfolios)

@app.route("/add", methods=["GET", "POST"])
def add_portfolio():
    if request.method == "POST":
        title = request.form["title"]
        link = request.form["link"]
        portfolio = Portfolio(title=title, link=link)
        db.session.add(portfolio)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add.html")

@app.route("/clear", methods=["GET"])
def clear_portfolios():
    Portfolio.query.delete()
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
