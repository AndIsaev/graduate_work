MOVIE_QUERY = f"""
                SELECT  
                        fw.id, 
                        fw.title, 
                        fw.description, 
                        fw.rating as imdb_rating, 
                        JSON_AGG(DISTINCT jsonb_build_object('id', g.id, 'name', g.name))
                                            FILTER (WHERE gfw.genre_id = g.id) AS genre,
                        JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'full_name', p.full_name)) 
                                            FILTER (WHERE pfw.role = 'actor') AS actors,
                        JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'full_name', p.full_name)) 
                                            FILTER (WHERE pfw.role = 'writer') AS writers,
                        JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'full_name', p.full_name)) 
                                            FILTER (WHERE pfw.role = 'director') AS directors,
                        GREATEST(fw.updated_at, MAX(g.updated_at), MAX(p.updated_at)) as updated_at
                FROM film_work as fw 
                        LEFT JOIN genre_film_work as gfw ON fw.id = gfw.film_work_id
                        LEFT JOIN genre as g ON (gfw.genre_id = g.id)
                        LEFT JOIN person_film_work as pfw ON (fw.id = pfw.film_work_id)
                        LEFT JOIN person as p ON (pfw.person_id = p.id)
                WHERE GREATEST(fw.updated_at, g.updated_at, p.updated_at) > '%s'
                GROUP BY fw.id
                ORDER BY GREATEST(fw.updated_at, MAX(g.updated_at), MAX(p.updated_at));
            """

GENRE_QUERY = """
                SELECT 
                        id,
                        name
                FROM genre
                WHERE updated_at > '%s'
                ORDER BY updated_at;
    """

PERSON_QUERY = """
                SELECT  p.id,
                        p.full_name,
                        ARRAY_AGG(DISTINCT pfw.role) AS roles,
                        JSON_AGG(DISTINCT jsonb_build_object('id', fw.id, 'title', fw.title)) 
                                    FILTER (WHERE pfw.film_work_id = fw.id) AS film_ids
                FROM person as p
                         LEFT JOIN person_film_work as pfw ON p.id = pfw.person_id
                         LEFT JOIN film_work as fw ON pfw.film_work_id = fw.id
                WHERE p.updated_at > '%s'
                GROUP BY p.id
                ORDER BY p.updated_at;
        """
