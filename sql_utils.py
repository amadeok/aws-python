import sqlite3 as sl


class sql_():
    def __init__(s) -> None:
        s.con = sl.connect('database_.db')
        s.cur = s.con.cursor()
        for row in s.cur.execute('''SELECT * FROM Main '''):
            print(row)
            s.add_aws_id(row[4])

    def get_row_from_aws_id(s, aws_id):
        sqlite_select_query = """SELECT * from Main where "aws-id" = ?"""
        s.cur.execute(sqlite_select_query, (aws_id,))
        record = s.cur.fetchone()
        if not record:
            print(f"aws-id {aws_id} not found")
            return None

        print("\nId: ", record[0])
        print("yt-id: ", record[1])
        print("region: ", record[2])
        print("mail: ", record[3])
        print("name : ", record[4])
        return record

    # array = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    # for row in array:
    #     cur.execute("INSERT INTO Uploads VALUES (?, ?, ?)", row)
    #cur.execute("UPDATE Uploads SET column_name = ? WHERE id = ?", ("new_value", 1))

    def add_track(s, track):
    # cur.fetchall()
        q = "SELECT EXISTS(SELECT 1 FROM Uploads WHERE __ = ?);"
        ret = s.cur.execute(q, (track,))
        result = s.cur.fetchone()[0]

        if result != 1:
            s.cur.execute("INSERT INTO Uploads DEFAULT VALUES")
            s.con.commit()
            s.cur.execute("UPDATE Uploads SET __ = ? WHERE rowid = (SELECT max(rowid) FROM Uploads);", (track, ))
            s.con.commit()
        else:
            print(f"database already contains {track}")

    def add_aws_id(s, id):
        try:
            s.cur.execute(f"ALTER TABLE Uploads ADD COLUMN '{id}' text")
            s.con.commit()
        except Exception as e:
            print(e)



    def set_record(s, col, row, val):
        s.cur.execute(f"UPDATE Uploads SET {col} = ? WHERE __ = ?;", (val, row ))
        #s.cur.execute(f"UPDATE Uploads SET new_aws_id = 1 WHERE rowid = 0;")
        s.con.commit()

    # qq = cur.execute("SELECT rowid, * FROM Uploads;")
    # for x in qq:
    #     print(x)

if __name__ == '__main__' :
    sql = sql_()
    exit()
    #q = "UPDATE Uploads SET __ = new_value1, new_aws_id = new_value2, ... WHERE rowid = (SELECT max(rowid) FROM Uploads);"
    #cur.execute("UPDATE Uploads SET __ = ? WHERE __ = ?", ("HELLO2", " "))
    #UPDATE table_name SET column1 = new_value1, column2 = new_value2, ... WHERE rowid = (SELECT max(rowid) FROM table_name);
    #cursor.execute("CREATE TABLE array_table (col1 INTEGER, col2 INTEGER, col3 INTEGER)")
    ret = sql.get_row_from_aws_id("ewaew")
    sql.add_track("01043.mp3")
    sql.set_record("new_aws_id2", "00023.mp3", 4 )
    sql.add_track("013.mp3")
    sql.set_record("new_aws_id2", "013.mp3", 13)
    sql.add_aws_id("dwad2")
    sql.add_track("022.mp3")
    sql.set_record("dwad", "022.mp3", 22 )
    ret = sql.get_row_from_aws_id("i-0f7cb6f8639cff05c")
    sql.add_track("099.mp3")
    sql.add_track("094.mp3")

    sql.set_record("dwad2", "094.mp3", 94 )