import pymysql

def run():
    pass
    db = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='helloworld',
        db='sys',
        charset='utf8')
    cursor = db.cursor()
    print(cursor.execute('CREATE DATABASE DB_TEST'))
    print(cursor.description)
    # print(cursor.execute('DROP DATABASE DB_TEST'))
    db.close()




if __name__ == '__main__':
    run()
