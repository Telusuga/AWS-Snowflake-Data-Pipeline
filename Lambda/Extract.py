import json
import requests
import pandas as pd
import zipfile
import pyarrow as pa
import pyarrow.parquet as pq
import io
import boto3


movie_list = [
    "The Shawshank Redemption", "The Godfather", "The Dark Knight", "Pulp Fiction", "Fight Club",
    "Forrest Gump", "Inception", "The Matrix", "The Lord of the Rings: The Return of the King",
    "Interstellar", "Gladiator", "The Silence of the Lambs", "Se7en", "Saving Private Ryan",
    "Schindler's List", "Whiplash", "The Prestige", "Parasite", "Django Unchained", "The Departed",
    "The Green Mile", "The Lion King", "Back to the Future", "The Pianist", "The Intouchables",
    "Avengers: Endgame", "Avengers: Infinity War", "Titanic", "Joker", "The Wolf of Wall Street",
    "The Social Network", "Good Will Hunting", "Braveheart", "Shutter Island", "No Country for Old Men",
    "A Beautiful Mind", "12 Angry Men", "The Truman Show", "Toy Story", "Toy Story 3",
    "WALL·E", "Up", "Inside Out", "Coco", "Monsters, Inc.", "Finding Nemo", "Ratatouille", "Cars",
    "The Incredibles", "Spirited Away", "Your Name", "Howl's Moving Castle", "Princess Mononoke",
    "My Neighbor Totoro", "Akira", "The Grand Budapest Hotel", "The Imitation Game", "The Theory of Everything",
    "Bohemian Rhapsody", "La La Land", "Black Panther", "Doctor Strange", "Iron Man", "Thor: Ragnarok",
    "Captain America: Civil War", "Logan", "Deadpool", "Guardians of the Galaxy", "Ant-Man",
    "The Maze Runner", "Divergent", "The Fault in Our Stars", "The Perks of Being a Wallflower",
    "500 Days of Summer", "Eternal Sunshine of the Spotless Mind", "Her", "Arrival", "Ex Machina",
    "Blade Runner 2049", "The Revenant", "Birdman", "Moonlight", "Manchester by the Sea",
    "The Big Short", "Spotlight", "The Shape of Water", "Roma", "Marriage Story",
    "Uncut Gems", "Everything Everywhere All At Once", "Oppenheimer", "Barbie", "Dune",
    "Tenet", "The Batman", "John Wick", "John Wick: Chapter 2", "Mad Max: Fury Road",
    "Inglourious Basterds", "The Hateful Eight", "Once Upon a Time in Hollywood", "The Irishman",
    "Knives Out", "Glass Onion", "Get Out", "Us", "Nope", "A Quiet Place", "Don't Look Up"
]

def lambda_handler(event, context):
    # TODO implement
    api_key = "67360a25"
    #movie = "Inception"
    movie_data=[]
    for movie in movie_list: 
        url = f"http://www.omdbapi.com/?i=tt3896198&apikey={api_key}&t={movie}"
        response = requests.get(url)
        data = response.json()
        movie_data.append(data)

    df = pd.DataFrame(movie_data)
    checks={}
    checks['source'] = 'OMDb API'
    checks['total_movies'] = len(df)
    checks['columns'] = str(list(df.columns))
    checks['primary_key'] = 'imdbID'
    checks['max_rating'] = df['imdbRating'].max()
    checks['min_rating'] = df['imdbRating'].min()
    checks['description'] = 'This dataset contains movie information fetched from the OMDb API.'
    output_buffer = io.BytesIO()
    table = pa.Table.from_pandas(df)
    pq.write_table(table, output_buffer)

    
    #print(output_buffer.getvalue())
    #print(type(output_buffer.getvalue()))
    try:
        #catalog = json.dumps(anime_data)
        s3_client = boto3.client('s3')
        s3_client.put_object(Body=output_buffer.getvalue(), Bucket='lambda-extract-test', Key='raw/test.parquet')
        s3_client.put_object(Body=json.dumps(checks), Bucket='lambda-extract-test', Key='raw/test.json')
        return {
        'statusCode': 200,
        'body': json.dumps('Data load is successful')
        }
    except Exception as e:
        return {
        'statusCode': 500,
        'body': json.dumps({"error": str(e)})
        }

