SELECT AVG(rating) FROM ratings JOIN movies WHERE ratings.movie_id = movies.id AND year = 2012;