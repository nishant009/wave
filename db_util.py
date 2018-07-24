import MySQLdb
import pydash as _

class DBUtil(object):
    def __init__(self, host=None, user=None, password=None, db=None):
        if (_.is_empty(host) or
            _.is_empty(user) or
            _.is_empty(db)
        ):
            raise RuntimeError('Database host or user or name missing. Please provide all three.')
        
        self._db = MySQLdb.connect(host, user, password, db)
        self._cursor = self._db.cursor()

    def close(self):
        self._cursor.close()
        self._db.close()

    def report_exists(self, report_id):
        count = self._cursor.execute(
            """SELECT report_id FROM reports WHERE report_id = %s""",
            (report_id,)
        )

        if count:
            return True
        else:
            return False

    def delete_report(self, report_id):
        try:
            self._cursor.execute(
                """DELETE FROM reports WHERE report_id = %s""",
                (report_id,)
            )
            self._db.commit()
        except:
            self._db.rollback()
            raise RuntimeError('Error persisiting report id')

    def persist_report(self, report_id):
        try:
            self._cursor.execute(
                """INSERT INTO reports (report_id) VALUES (%s)""",
                (report_id,)
            )
            self._db.commit()
        except:
            self._db.rollback()
            raise RuntimeError('Error persisiting report id')

    def populate_payroll(self, values):
        try:
            self._cursor.executemany(
                """INSERT INTO payroll (employee_id, date, hours, job_group) VALUES (%s, %s, %s, %s)""",
                values
            )
            self._db.commit()
        except Exception as e:
            print(e)
            self._db.rollback()
            raise RuntimeError('Error persisiting values')

    def get_report_data(self):
        self._cursor.execute(
            """SELECT date, employee_id, hours, job_group FROM payroll ORDER BY employee_id ASC, date DESC"""
        )

        return self._cursor.fetchall()