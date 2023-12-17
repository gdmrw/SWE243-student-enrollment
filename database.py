from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector
from mysql.connector import errorcode



def check_enrollment(id):
    cnx = mysql.connector.connect(user='root', database='student_course_enroll', password='password')
    cursor = cnx.cursor()
    query = ("SELECT c.course_name from student AS s, student_course AS sc, course AS c "
             "where s.id = sc.student_id and sc.course_id = c.id and s.id = %s ")

    cursor.execute(query, (id,))
    result = cursor.fetchall()
    if result is not None:
        print("You now enrolled in these course below:")
        for course_name in result:
            print(course_name[0])
    else:
        print("You're not enroll any course now")

    cursor.close()
    cnx.close()

def display_course():
    cnx = mysql.connector.connect(user='root', database='student_course_enroll', password='password')
    cursor = cnx.cursor()
    query = ("select id, course_name, course_hour, day_of_week from course")
    cursor.execute(query)
    result = cursor.fetchone()
    while result is not None:
        (id ,name, time, week_of_day) = result
        time_convert = "{:0>8}".format(str(time))
        print(f"course id: {id}, course name: {name}, course hour: {time_convert} in {week_of_day}")
        result = cursor.fetchone()

    # for (course_name, course_hour, day_of_week) in cursor:
    #     print("course id:{} course name:{} started at {} in {}".format(
    #         id,course_name, course_hour, day_of_week))
    cursor.close()
    cnx.close()

def course_enroll(uid_student):
    """

    :param uid_student:  student primary key
    :return:
    """
    cnx = mysql.connector.connect(user='root', database='student_course_enroll', password='yourpassword')
    cursor = cnx.cursor()
    print('These are the courses available now, which one you want to enroll')
    display_course()
    result = input('\ttype course id: ')  # target course id
    insertion = "INSERT INTO student_course VALUES (default,%s,%s)"
    try:
        cursor.execute(insertion,(uid_student,result))
        print("Enrollment succeed")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DUP_ENTRY:
            print("Enrollment failed! You have already in this course, please check your enrollment")
        elif err.errno == errorcode.ER_NO_REFERENCED_ROW_2 or errorcode.ER_NO_REFERENCED_ROW:
            print("Enrollment failed! The course id do not exist")
        else:
            print(err)
    cnx.commit()
    cursor.close()
    cnx.close()


def check_course_calendar(id): #student primary key
    cnx = mysql.connector.connect(user='root', database='student_course_enroll', password='yourpassword')
    cursor = cnx.cursor()
    print("which day you want to check?")
    result = input('\ttype in Monday - Sunday: ')
    week = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    if result.lower() not in week:
        print("query failed, please enter legal day of week")
        return
    query = ("SELECT  c.course_name, c.course_hour from student AS s, student_course as sc, course as c "
             "where s.id = sc.student_id and sc.course_id = c.id and s.id = %s and c.day_of_week = %s ")

    cursor.execute(query,(id,result))
    exc_ret = cursor.fetchone()
    if not exc_ret:
        print(f"you have no course this {result}")
    else:
        print(f"you have course in {result}:")
    while exc_ret:  # exc_ret == execution result
        (course_name, course_hour) = exc_ret
        time_convert = "{:0>8}".format(str(course_hour))
        print(f"you have course ->{course_name}<-, started at {time_convert} this {result}")
        exc_ret = cursor.fetchone()

    cursor.close()
    cnx.close()


def student_registration():
    cnx = mysql.connector.connect(user='root', database='student_course_enroll', password='yourpassword')
    cursor = cnx.cursor()

    print("---------welcome to student registration plaform----------")
    print("type 'R' if you want to return to student menu")
    name = input('\tEnter your name: ')
    id = input('\tEnter your student id: ')
    if name == "R" or id == "R":
        cursor.close()
        cnx.close()
        return

    insertion = "INSERT INTO student VALUES (DEFAULT, %s, %s) "

    try:
        cursor.execute(insertion,(name,id))
        print("Registration succeed!")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DUP_ENTRY:
            print("Failed! Student already register, please login")
        else:
            print(err)

    cnx.commit()
    cursor.close()
    cnx.close()


def new_course():
    cnx = mysql.connector.connect(user='root', database='student_course_enroll', password='password')
    cursor = cnx.cursor()
    print("Please fill in the course information according to the prompts")
    print("If you want to quit, please type 'Q'")
    course_name = input('Please enter course name:')
    course_time = input('Please enter class time, format: 00:00:00: ')
    course_day_of_week = input('Please enter day of week, format: Monday to Sunday: ')

    insertion = "INSERT INTO course VALUES (DEFAULT, %s,%s,%s)"

    if course_name == "Q" or course_time == "Q" or course_day_of_week == "Q":
        print("exit")
        return

    try:
        cursor.execute(insertion, (course_name, course_time, course_day_of_week))
        print("course add succeed")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DUP_ENTRY:
            print("failed! course already in the list")
        elif err.errno == errorcode.WARN_DATA_TRUNCATED:
            print("failed! please enter valid week ")
        else:
            print(err)

    cnx.commit()
    cursor.close()
    cnx.close()


def student_in_course():
    cnx = mysql.connector.connect(user='root', database='student_course_enroll', password='password')
    cursor = cnx.cursor()

    print("enter the course id you want to check")
    display_course()
    result = input('id: ')

    query = ("SELECT s.name AS student_name, s.student_id FROM student AS s JOIN student_course AS sc ON s.id = "
             "sc.student_id JOIN course AS c ON sc.course_id = c.id WHERE c.id = %s ORDER BY s.name;")

    cursor.execute(query,(result,))

    exc_ret = cursor.fetchone()
    if not exc_ret:
        print(f"no student enroll in this course yet")
    else:
        print("below are students enroll in this course")
    while exc_ret:  # exc_ret == execution result
        (student_name, student_id) = exc_ret
        print(f"student: {student_name} id: {student_id}")
        exc_ret = cursor.fetchone()

    cursor.close()
    cnx.close()












if __name__ == '__main__':
    # check_enrollment(1)
    # display_course()
    # course_enroll(1)
    # check_course_calendar(1)
    # student_registration()
    # new_course()
    student_in_course()








