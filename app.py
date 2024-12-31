from flask import Flask, render_template, request
import pickle
import numpy

famous_books=pickle.load(open('models/famous.pkl','rb'))

books=pickle.load(open('models/books.pkl','rb'))

colabFiltering=pickle.load(open('models/colabFiltering.pkl','rb'))

similarity_scores=pickle.load(open('models/similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                        book_name=list(famous_books['Book-Title'].values),
                        author=list(famous_books['Book-Author'].values),
                        image=list(famous_books['Image-URL-M'].values),
                        votes=list(famous_books['RatingCount'].values),
                        rating=list(famous_books['RatingMean'].values))

@app.route('/authorSimilarity')
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

# COLABBORATIVE FILTERING
@app.route('/colabFilteringSimilarity')
def colabFilterSimilarity():
    return render_template('colabFilter.html')

@app.route('/colabFiltered',methods=['POST'])
def colabFilteredBooks():
    # return 'Hello Humaid'
    user_input = request.form.get('user_input')
    index = numpy.where(colabFiltering.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == colabFiltering.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Author')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Image-URL-M')['Image-URL-M'].values))

        data.append(item)

    # print(data)

    return render_template('colabFilter.html',data=data)


if __name__=='__main__':
    app.run(debug=True)