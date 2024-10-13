from flask import Flask, render_template, request
import pickle

famous_books=pickle.load(open('models/famous.pkl','rb'))

books=pickle.load(open('models/books.pkl','rb'))

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

@app.route('/similarAuthors',methods=['POST'])
def similar_authors():
    author_name=request.form.get('authorName')
    desiredBooks = books[books['Book-Author']==author_name]
    # return desiredBooks.to_dict(orient="records")
    data=desiredBooks.to_dict(orient="records")
    return render_template("similarity.html",
                        book_name=list(desiredBooks['Book-Title'].values),
                        image=list(desiredBooks['Image-URL-M'].values))


if __name__=='__main__':
    app.run(debug=True)