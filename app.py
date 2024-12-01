import datetime
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os
from dotenv import load_dotenv # needed for running on render.com, we load in some variables from a the file we called .env (which is a hidden file)

load_dotenv() # import all variables from our hidden file .env (dot = .), or if we are on render.com via a separate file called .env.

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.RodgeBlog

    @app.route("/", methods=["GET", "POST"])
    def home():    
        if request.method == "POST":
            if request.form.get("content") != '':
                entry_content = request.form.get("content") # name of the field
                formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")

                print(entry_content, formatted_date) # printed in the console (tip for checking if stuff works!!)

                app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]
        if request.method == "POST":
            return redirect(url_for("home", entries=entries_with_date))
        else:    
            return render_template("home.html", entries=entries_with_date)  
        
    if __name__ == "__main__":
        app.run(debug=True) #with debut =True change will be noticed in de server, and you dont have to rerun the code all 
    
    return app
 