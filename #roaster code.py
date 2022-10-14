
import json
import sqlite3

#creating database
dbname = "roster.sqlite"
conn = sqlite3.connect(dbname)
cur = conn.cursor()

cur.executescript('''
            DROP TABLE IF EXISTS user;
            DROP TABLE IF EXISTS course;
            DROP TABLE IF EXISTS member;
            
            
            CREATE TABLE user(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                name TEXT UNIQUE
            );
            CREATE TABLE course(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                title TEXT UNIQUE
            );
            CREATE TABLE memebr(
                user_id INTEGER,
                course_id INTEGER,
                role INTEGER,
                PRIMARY KEY(user_id, course_id)
            );
            ''')


#deserializing the data
filename = "roster_data.json"
jsondata = open(filename)
data = json.load(jsondata)

#PART 3: INSERTING DATA
for entry in data:
	user = entry[0]
	course = entry[1]
	instructor = entry[2]

	#Inserting user
	user_statement = """INSERT OR IGNORE INTO User(name) VALUES( ? )"""
	SQLparams = (user, )
	cur.execute(user_statement, SQLparams)

	#Inserting course
	course_statement = """INSERT OR IGNORE INTO Course(title) VALUES( ? )"""
	SQLparams = (course, )
	cur.execute(course_statement, SQLparams)

	#Getting user and course id
	courseID_statement = """SELECT id FROM Course WHERE title = ?"""
	SQLparams = (course, )
	cur.execute(courseID_statement, SQLparams)
	courseID = cur.fetchone()[0]

	userID_statement = """SELECT id FROM User WHERE name = ?"""
	SQLparams = (user, )
	cur.execute(userID_statement, SQLparams)
	userID = cur.fetchone()[0]

	#Inserting the entry
	member_statement = """INSERT INTO Member(user_id, course_id, role)
		VALUES(?, ?, ?)"""
	SQLparams = (userID, courseID, instructor)
	cur.execute(member_statement, SQLparams)

#Saving the changes
conn.commit()

#PART 4: Testing and obtaining the results
test_statement = """
SELECT hex(User.name || Course.title || Member.role ) AS X FROM 
    User JOIN Member JOIN Course 
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY X
"""
cur.execute(test_statement)
result = cur.fetchone()
print("RESULT: " + str(result))

#Closing the connection
cur.close()
conn.close()
