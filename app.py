from flask import Flask, render_template
import pickle

famous_books=pickle.load(open('models/famous.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(famous_books['Book-Title'].values),
                           author=list(famous_books['Book-Author'].values),
                           image=list(famous_books['Image-URL-M'].values),
                           votes=list(famous_books['RatingCount'].values),
                           rating=list(famous_books['RatingMean'].values))

@app.route('/similarity')
def similarity():
    return render_template('similarity.html')

if __name__=='__main__':
    app.run(debug=True)