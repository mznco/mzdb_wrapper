import psycopg2
import logging

# Inherit logging
logger = logging.getLogger('root')


class pgdb(object):
    def __init__(self, user, password, host, database):
        try:
            self.pgdb_cnx = psycopg2.connect(user=user, password=password,
                                             host=host, database=database)
            self.pgdb_cursor = self.pgdb_cnx.cursor()

        except Exception as e:
            logging.error("pgdb: __init__ exception: %s" % e)

    def close(self):
        self.pgdb_cnx.close()

    def exec_sql(self, sql):
        try:
            sql.replace("'", "").replace('"', "")  # Sanitize inputs.
            # TODO more injection protection
            if sql[-1] != ';':
                sql = sql + ';'
            logging.debug("pgdb: exec_sql: SQL statement: \n%s" % sql)
            self.pgdb_cursor.execute(sql)
            self.pgdb_cnx.commit()
            try:
                return self.pgdb_cursor.fetchall()
            except psycopg2.ProgrammingError as e:
                logging.info('pgdb: exec_sql: No data returned')
                return True
        except Exception as e:
            logging.debug("pgdb: exec_sql: exception: %s" % e)
            return None
