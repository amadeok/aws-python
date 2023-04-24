import sqlite3 as sl
import logging
import os, shutil

class sql_():
    def __init__(s) -> None:
        s.con = sl.connect('database_.db')
        s.cur = s.con.cursor()
        for row in s.cur.execute('''SELECT * FROM Main '''):
            logging.info(row)
            s.add_update_table_col(row[3])

    def get_row(s, input : str, use_name : bool = True):
        sqlite_select_query = f"""SELECT * from Main where "{"name" if use_name else "aws-id"}" = ?"""
        s.cur.execute(sqlite_select_query, (input,))
        record = s.cur.fetchone()
        if not record:
            logging.info(f"{'name' if use_name else 'aws-id'} {input} not found")
            return None

        # logging.info(f"\nId: {record[0]}")
        # logging.info(f"yt-id: {record[1]}")
        # logging.info(f"region: {record[2]}")
        # logging.info(f"name : {record[3]}")
        # logging.info(f"tt_mail: {record[4]}")
        # logging.info(f"yt_mail: {record[5]}")

        return record

    # array = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    # for row in array:
    #     cur.execute("INSERT INTO Uploads VALUES (?, ?, ?)", row)
    #cur.execute("UPDATE Uploads SET column_name = ? WHERE id = ?", ("new_value", 1))

    def add_track(s, track):
    # cur.fetchall()
        for table_name in ("TT_Uploads", "YT_Uploads"):
            q = f"SELECT EXISTS(SELECT 1 FROM {table_name} WHERE __ = ?);"
            ret = s.cur.execute(q, (track,))
            result = s.cur.fetchone()[0]

            if result != 1:
                s.cur.execute(f"INSERT INTO {table_name} DEFAULT VALUES")
                s.con.commit()
                s.cur.execute(f"UPDATE {table_name} SET __ = ? WHERE rowid = (SELECT max(rowid) FROM {table_name});", (track, ))
                s.con.commit()
            else:
                logging.info(f"database already contains {track}")

    def add_update_table_col(s, name):
        for table_name in ("TT_Uploads", "YT_Uploads"):
            try:
                s.cur.execute(f"ALTER TABLE {table_name} ADD COLUMN '{name}' text")
                s.con.commit()
            except Exception as e:
                logging.info(e)



    def set_record(s, col, row, val, table):
        s.cur.execute(f"""UPDATE {table} SET "{col}" = ? WHERE __ = ?;""", (val, row ))
        #s.cur.execute(f"UPDATE Uploads SET new_aws_id = 1 WHERE rowid = 0;")
        s.con.commit()
    
    def get_record(s, col, row, table):
        try:
            s.cur.execute(f""" SELECT  "{col}" FROM  {table} WHERE "__" = "{row}" """)
        except Exception as e:
            logging.info(e)
            return None
        record = s.cur.fetchone()
        if not record or record[0] == col:
            logging.info(f"not found: col {col} row {row} table {table} ")
            return None
        return record[0]


if __name__ == '__main__' :
    sql = sql_()
    print(sql.get_record("virg0","00003(4).wav", "TT_Uploads"))
    print(sql.get_record("melb0","00003(4).wav", "TT_Uploads"))
    print(sql.get_record("melb0","00002(5).wav", "TT_Uploads"))
    print(sql.get_record("virg0","00002(5).wav", "TT_Uploads"))
    print(sql.get_record("Non5e","00002(5).wav", "TT_Uploads"))

    sql.get_row("melb0", use_name=True)
    exit()
    #q = "UPDATE Uploads SET __ = new_value1, new_aws_id = new_value2, ... WHERE rowid = (SELECT max(rowid) FROM Uploads);"
    #cur.execute("UPDATE Uploads SET __ = ? WHERE __ = ?", ("HELLO2", " "))
    #UPDATE table_name SET column1 = new_value1, column2 = new_value2, ... WHERE rowid = (SELECT max(rowid) FROM table_name);
    #cursor.execute("CREATE TABLE array_table (col1 INTEGER, col2 INTEGER, col3 INTEGER)")
    ret = sql.get_row("ewaew")
    sql.add_track("01043.mp3")
    sql.set_record("new_aws_id2", "00023.mp3", 4 )
    sql.add_track("013.mp3")
    sql.set_record("new_aws_id2", "013.mp3", 13)
    sql.add_update_table_col("dwad2")
    sql.add_track("022.mp3")
    sql.set_record("dwad", "022.mp3", 22 )
    ret = sql.get_row("i-0f7cb6f8639cff05c")
    sql.add_track("099.mp3")
    sql.add_track("094.mp3")

    sql.set_record("dwad2", "094.mp3", 94 )



def delete_file(file_path):
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

def delelte_files_in_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        delete_file(file_path)