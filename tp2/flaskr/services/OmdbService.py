class OmdbService(object):
    def __init__(self, omdb_gateway):
        self.omdb_gateway = omdb_gateway

    def all(self, movie):
        return self.omdb_gateway.movie(movie=movie)

    def genre(self, movie):
        movie_json = self.omdb_gateway.movie(movie=movie)
        return movie_json['Genre']

    def actors(self, movie):
        movie_json = self.omdb_gateway.movie(movie=movie)
        print(movie_json)
        return movie_json['Actors']

    def plot(self, movie):
        movie_json = self.omdb_gateway.movie(movie=movie)
        return movie_json['Plot']

    def language(self, movie):
        movie_json = self.omdb_gateway.movie(movie=movie)
        return movie_json['Language']

    def anio(self, movie):
        movie_json = self.omdb_gateway.movie(movie=movie)
        return movie_json['Year']

    def duracion(self, movie):
        movie_json = self.omdb_gateway.movie(movie=movie)
        return movie_json['Runtime']

    def awards(self, movie):
        movie_json = self.omdb_gateway.movie(movie=movie)
        return movie_json['Awards']

    def poster(self, movie):
        movie_json = self.omdb_gateway.movie(movie=movie)
        return movie_json['Poster']

    def ratings(self, movie):
        movie_json = self.omdb_gateway.movie(movie=movie)
        return movie_json['Ratings']

    def imdb_votes(self, movie):
        movie_json = self.omdb_gateway.movie(movie=movie)
        return movie_json['imdbVotes']

    def production(self, movie):
        movie_json = self.omdb_gateway.movie(movie=movie)
        return movie_json['Production']
