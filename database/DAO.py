from database.DB_connect import DBConnect


class DAO():


    @staticmethod
    # ----------------------  RECUPERA I VALORI RATING
    def get_all_rating():
        conn = DBConnect.get_connection()
        result = []

        if conn is None:
            return result

        try:
            cursor = conn.cursor(dictionary=True)
            query= """  SELECT DISTINCT avg_rating
                        FROM ratings
                        ORDER BY avg_rating ASC
                    """

            cursor.execute(query)

            for row in cursor:
                result.append(row["avg_rating"])

            cursor.close()
            conn.close()

        except Exception as e:
            print(f"Errore nel metodo get_all_rating: {e}")

            if conn:
                conn.close()
        return result

    @staticmethod
    #-------------------------- VERTICI DEL GRAFO
    def get_attori_per_range(rating_min, rating_max):
        conn = DBConnect.get_connection()
        result=[]

        if conn is None:
            return result

        try:
            cursor = conn.cursor(dictionary=True)
            query=""" SELECT DISTINCT n.id, n.name, n.date_of_birth
                      FROM names n 
                      JOIN role_mapping rm ON n.id = rm.name_id
                      JOIN movie m ON m.id = rm.movie_id
                      JOIN ratings r ON m.id = r.movie_id
                      WHERE r.avg_rating BETWEEN %s AND %s
                      AND rm.category IN ('actor', 'actress')
                  """

            cursor.execute(query, (rating_min, rating_max))

            for row in cursor:
                result.append((row["id"], row["name"], row["date_of_birth"]))

            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Errore nel metodo get_attori_per_range: {e}")
            if conn:
                conn.close()

        return result

    @staticmethod
    # ARCHI
    def get_incassi_film_comuni(rating_min, rating_max):

        conn=DBConnect.get_connection()
        result=[]

        if conn is None:
            return result

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                    SELECT DISTINCT rm1.name_id AS id1, rm2.name_id AS id2, m.worlwide_gross_income AS incasso
                    FROM role_mapping rm1
                    JOIN role_mapping rm2 ON rm1.movie_id = rm2.movie_id
                    JOIN movie m ON rm1.movie_id = m.id
                    JOIN ratings r ON m.id = r.movie_id
                    WHERE r.avg_rating BETWEEN %s AND %s
                    AND rm1.category IN ('actor', 'actress')
                    AND rm2.category IN ('actor', 'actress')
                    AND rm1.name_id < rm2.name_id
                    """
            cursor.execute(query,(rating_min, rating_max))

            for row in cursor:
                result.append((row["id1"], row["id2"], row["incasso"]))

            cursor.close()
            conn.close()

        except Exception as e:
            print(f"Errore nel metodo get_incassi_film_comuni: {e}")
            if conn:
                conn.close()

        return result


