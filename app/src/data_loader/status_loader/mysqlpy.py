import pymysql.cursors

connection = pymysql.connect(host='79.175.176.165',
                             user='admin',
                             password='vwB75K',
                             database='trade_db',
                             cursorclass=pymysql.cursors.DictCursor)

with connection:
    #with connection.cursor() as cursor:
        # Create a new record
        #sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        #cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    #connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT version()"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)