from database.DB_connect import DBConnect

from model.Actor import Actor

class DAO():

    @staticmethod
    def getAllRatings():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct avg_rating  FROM ratings r  ORDER BY avg_rating "

        cursor.execute(query)

        for row in cursor:
            results.append(row["avg_rating"])

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getAllActorsbyRange(rat1, rat2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct rm.name_id as ActorID, n.name as Name, n.date_of_birth as birth_date
                    from movie m, role_mapping rm, ratings r, names n 
                    where n.id = rm.name_id 
                    and n.date_of_birth IS NOT NULL
                    and m.id = rm.movie_id 
                    and m.id = r.movie_id 
                    and r.avg_rating >= %s
                    and r.avg_rating <= %s"""

        cursor.execute(query, (rat1,rat2))

        for row in cursor:
            results.append(Actor(**row))

        cursor.close()
        conn.close()
        return results



    @staticmethod
    def getAllEdges(rat1, rat2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select rm1.name_id as Actor1, rm2.name_id as Actor2, sum( cast(replace(replace(m.worlwide_gross_income, '$', ''),',', '') as unsigned)) as Weight
                    from movie m, role_mapping rm1, role_mapping rm2, ratings r, names n1, names n2
                    where m.id = rm1.movie_id
                    and m.id = rm2.movie_id
                    and m.id = r.movie_id
                    and rm1.name_id = n1.id
                    and rm2.name_id = n2.id
                    and n1.date_of_birth IS NOT NULL
                    and n2.date_of_birth IS NOT NULL
                    and rm1.name_id < rm2.name_id
                    and r.avg_rating >= %s
                    and r.avg_rating <= %s
                    and m.worlwide_gross_income is not null
                    and m.worlwide_gross_income like '$%'
                    group by rm1.name_id, rm2.name_id"""

        cursor.execute(query, (rat1,rat2))

        for row in cursor:
            results.append((row['Actor1'], row['Actor2'], row['Weight']))

        cursor.close()
        conn.close()
        return results