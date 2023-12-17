from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector
import database

def main_menu():
    while True:
        print("\nWelcome to the Course Enroll Interface")
        print("-----------------------------------")
        print("1.Student")
        print("2.Teacher")
        print("3.Registration")
        print("Q.Quit\n")
        print("-----------------------------------")
        choice = input('\tplease select:')
        if choice == "1":
            secondary_menu_student()
            return
        elif choice == "2":
            teacher_menu()
            return
        elif choice == "3":
            database.student_registration()

        elif choice == "Q":
            print("bye!")
            return
        else:
            print('error, no such item, please type again')
            main_menu()
            return

def secondary_menu_student():
    cnx = mysql.connector.connect(user='root', database='student_course_enroll', password='yourpassword')
    cursor = cnx.cursor()

    query = ("SELECT id,s.name FROM student AS s where s.name = %s AND s.student_id = %s")

    print("please enter your name and your student ID")
    name = input('\tName:')
    student_id = input('\tstudent id:')

    cursor.execute(query,(name,student_id))
    result = cursor.fetchone()
    if result is not None:
        third_menu_student(result[0],name) # result[0] is the student primary key
    else:
        print("the name or student id you type are wrong, if you new please register first")
        main_menu()
    cursor.close()
    cnx.close()


def third_menu_student(id,name):
    """
    :param id: student primary key
    :param name:
    :return:
    """
    while True:
        print("\nStudent Course enrollment")
        print(f"Hello {name}, what do you want to do?")
        print("-----------------------------------")
        print("1.check what you enrolled")
        print("2.make an enrollment")
        print("3.check your course calendar")
        print("4.back to main menu")
        print("Q.Quit")
        print("-----------------------------------")
        result = input('\tmake your choice:')

        if result == "1":
            database.check_enrollment(id)
        elif result =="2":
            database.course_enroll(id)
        elif result =="3":
            database.check_course_calendar(id)
        elif result =="4":
            main_menu()
            return
        elif result =="Q":
            print("Bye!")
            return
        else:
            print("wrong enter, please enter again")
            third_menu_student(id,name)
            return

def teacher_menu():
    while True:
        print("----------Welcome to the teacher control interface-----------")
        print("1.introduce new course")
        print("2.query course enrollment status")
        print("3.back to main menu")
        print("Q.Quit")
        print("---------------------------------------")
        result = input('\tType to choose: ')

        if result == "1":
            database.new_course()
        elif result == "2":
            database.student_in_course()
        elif result == "3":
            main_menu()
            return
        elif result == "Q":
            print("Bye!")
            return
        else:
            print("wrong enter, please enter again")
            teacher_menu()
            return





main_menu()

