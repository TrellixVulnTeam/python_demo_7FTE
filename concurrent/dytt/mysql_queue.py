# -*- coding: utf-8 -*-

import pymysql
import sys

def create_table(conn):
    sql_drop_table = "drop table if EXISTS movies;"
    sql_create_table = "create table if not exists movies(" \
                       "_id int auto_increment," \
                       "name_cn varchar(128)," \
                       "name varchar(128)," \
                       "year varchar(16)," \
                       "country varchar(64)," \
                       "category varchar(128)," \
                       "language varchar(64)," \
                       "subtitle varchar(64)," \
                       "release_date varchar(64)," \
                       "score varchar(256)," \
                       "file_count varchar(128)," \
                       "duration varchar(64)," \
                       "director varchar(128)," \
                       "download_url text," \
                       "primary key(_id)" \
                       ")"
    cursor = conn.cursor()
    try:
        cursor.execute(sql_drop_table)
        cursor.execute(sql_create_table)
        conn.commit()
    except:
        conn.rollback()


def load_data(conn, data_path):
    cursor = conn.cursor()
    sql_load_data = 'load data local infile \'{0}\' into table movies ' \
                    'fields terminated by \';\' enclosed by \'"\' ' \
                    'lines terminated by \'\n\' ' \
                    '(name_cn,name,year,country,category,language,subtitle,' \
                    'release_date,score,file_count,duration,director,download_url)'.format(data_path)
    try:
        cursor.execute(sql_load_data)
        conn.commit()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        conn.rollback()

if __name__ == '__main__':
    connection = pymysql.connect("localhost", "root", "root", "TESTDB", local_infile=1)
    create_table(connection)
    path = 'data/movies_queue.txt'
    load_data(connection, path)
    connection.close()
