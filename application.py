mport pickle
from crypt import methods
from flask import Flask,render_template,request


app = Flask(__name__)


top_100 = pickle.load(open("top_100.pkl","rb"))
similarity = pickle.load(open("similarity.pkl","rb"))
movies = pickle.load(open("movies.pkl","rb"))



top_data = []

for i in top_100["index"]:
    val = top_100[top_100["index"]==i].values[0]
    top_data.append(val)



@app.route("/",methods=["GET","POST"])
def home():
    return render_template("home.html",top = top_data)







@app.route("/recommand",methods=["GET","POST"])
def recommand():

    datas = []
    indexes_of_5_movies=None
    movie_index = None

    if request.method == "POST":
        movie_name = request.form.get('movie')

        if movie_name not in movies["Title"].values:
            error_msg = "please enter a valid movie name"
            return render_template("error.html", msg=error_msg)

        movie_index = movies[movies["Title"] == movie_name].index[0]
        distances = similarity[movie_index]
        indexes_of_5_movies = sorted(list(enumerate(distances)),reverse=True, key=lambda x:x[1])[1:6]

        for i in indexes_of_5_movies:
            datas.append(movies.iloc[i[0],1:-1].values)

    return render_template("recommand.html",name = datas,top = top_data)





if __name__=="__main__":
    app.run(debug=True,port=5003)