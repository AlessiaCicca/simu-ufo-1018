from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.stato import Stato


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAnni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct year(s.`datetime`) as anno
from sighting s"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["anno"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getForme(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct s.shape  as forma
from sighting s 
where year(s.`datetime` )= %s
order by s.shape"""

        cursor.execute(query,(anno,))

        for row in cursor:
            result.append(row["forma"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct *
                       from state s """

        cursor.execute(query)

        for row in cursor:
            result.append(Stato(**row))

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getConnessioni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct n.state1 as v1, n.state2 as v2
from neighbor n 
where n.state1<n.state2"""

        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPeso(forma, anno, stato1, stato2):
        conn = DBConnect.get_connection()

        result = 0

        cursor = conn.cursor(dictionary=True)
        query = """select count(*) as peso
                       from sighting s 
                       where s.shape=%s and year(s.`datetime`)=%s and (s.state=%s or s.state=%s)
                        """

        cursor.execute(query, (forma, anno, stato1, stato2,))

        for row in cursor:
            result = row["peso"]

        cursor.close()
        conn.close()
        return result