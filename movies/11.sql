SELECT title FROM movies JOIN stars, ratings, people WHERE movies.id = stars.movie_id AND ratings.movie_id = stars.movie_id AND stars.person_id = people.id AND name = "Chadwick Boseman" ORDER BY -rating LIMIT 5;