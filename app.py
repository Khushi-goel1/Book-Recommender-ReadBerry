from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                            book_name = list(popular_df['Book-Title'].values),
                            # author = list(popular_df['Book-Author'].values),
                            image = list(popular_df['Image-URL-M'].values),
                            # votes = list(popular_df['num_ratings'].values),
                            # rating = list(popular_df['avg_ratings'].values)
                           )

def recommend(book_name):
    # index fetch
    try:
        index = np.where(pt.index == book_name)[0][0]
    except IndexError:
        return []

    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append({
            'title': item[0],
            'image': item[1],
        })
    return data

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    preference = data['preference']

    recommended_books = recommend(preference)
    if not recommended_books:
        recommended_books = [{'title': 'No recommendations found', 'image': ''}]

    return jsonify({'recommendations': recommended_books})

if __name__ == '__main__':
    app.run(debug=True)