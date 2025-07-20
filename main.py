import pandas as pd
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
from surprise import accuracy

ratings = pd.read_csv(
    'BX-Book-Ratings.csv',
    sep=';',
    encoding='latin-1'
)
ratings.rename(
    columns={
        'User-ID': 'user_id',
        'ISBN': 'book_id',
        'Book-Rating': 'rating'
    },
    inplace=True
)

books = pd.read_csv(
    'BX-Books.csv',
    sep=';',
    encoding='latin-1'
)
books.rename(
    columns={
        'ISBN': 'book_id',
        'Book-Title': 'title'
    },
    inplace=True
)

books = books[['book_id', 'title']]

user_counts = ratings['user_id'].value_counts()
ratings = ratings[
    ratings['user_id'].isin(
        user_counts[user_counts >= 50].index
    )
].reset_index(drop=True)

reader = Reader(rating_scale=(0, 10))
data = Dataset.load_from_df(
    ratings[['user_id', 'book_id', 'rating']],
    reader
)

trainset, testset = train_test_split(
    data,
    test_size=0.2,
    random_state=42
)

model = SVD()
model.fit(trainset)

predictions = model.test(testset)
accuracy.rmse(predictions) 

def recomendar_svd(user_id, n=5):
    lidos = ratings[
        ratings['user_id'] == user_id
    ]['book_id'].unique()

    todos = ratings['book_id'].unique()
    
    nao_lidos = [b for b in todos if b not in lidos]
    
    preds = [
        (bid, model.predict(user_id, bid).est)
        for bid in nao_lidos
    ]
    preds.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\nTop {n} recomendações para usuário {user_id}:")
    for bid, score in preds[:n]:
        tit = books.loc[
            books['book_id'] == bid, 'title'
        ].values
        if tit.size:
            print(f"- {tit[0]} (score: {score:.2f})")
        else:
            print(f"- ISBN {bid} (score: {score:.2f})")

recomendar_svd(user_id=276729, n=5)
