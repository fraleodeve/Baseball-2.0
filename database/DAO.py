from database.DB_connect import DBConnect
from model.giocatore import Giocatore
from model.team import Team

class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct(a.`year`) as anno
                    from appearances a  """

        cursor.execute(query)

        for row in cursor:
            result.append(row["anno"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllPlayers():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                        from people p  """

        cursor.execute(query)

        for row in cursor:
            result.append(Giocatore(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodes(anno, salario):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select p.playerID as ID
                    from people p, salaries s, teams t 
                    where p.playerID = s.playerID and s.teamID = t.ID and s.`year` = %s and s.salary > %s
                    group by p.playerID, t.ID, s.`year`  """

        cursor.execute(query, (anno, salario))

        for row in cursor:
            result.append(row["ID"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(anno, salario):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.playerID as p1, t2.playerID as p2
                    from (select p.playerID, a.teamID 
                    from appearances a, people p, salaries s, teams t 
                    where p.playerID = a.playerID 
                    and p.playerID = s.playerID 
                    and a.teamID = t.ID 
                    and s.`year` = %s 
                    and a.`year` = %s 
                    and s.salary > %s) t1,
                    (select p.playerID, a.teamID 
                    from appearances a, people p, salaries s, teams t 
                    where p.playerID = a.playerID 
                    and p.playerID = s.playerID 
                    and a.teamID = t.ID 
                    and s.`year` = %s 
                    and a.`year` = %s 
                    and s.salary > %s) t2
                    where t1.teamID = t2.teamID and t1.playerID > t2.playerID
                    group by t1.playerID, t2.playerID """

        cursor.execute(query, (anno, anno, salario, anno, anno, salario))

        for row in cursor:
            result.append((row["p1"], row["p2"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def ricorsione(anno, salario):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select p.playerID as p, a.teamID as t, s.salary as s
                    from appearances a, people p, salaries s, teams t 
                    where p.playerID = a.playerID 
                    and p.playerID = s.playerID 
                    and a.teamID = t.ID 
                    and s.`year` = %s 
                    and a.`year` = %s
                    and s.salary > %s  """

        cursor.execute(query, (anno, anno, salario))

        for row in cursor:
            result.append((row["p"], row["t"], row["s"]))

        cursor.close()
        conn.close()
        return result