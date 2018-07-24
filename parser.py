import csv
import pydash as _

from datetime import datetime
from db_util import DBUtil

class Parser(object):
    def __init__(self, db_util, file_name):
        if _.is_empty(db_util) or _.is_empty(file_name):
            raise RuntimeError('DB Util object or CSV file name missing. Please provide both.')
        if  not isinstance(db_util, DBUtil):
            raise RuntimeError('DB Util object is not of the correct type')

        self._db_util = db_util
        self._file = file_name
        self._data = []

    def _read_csv(self):
        with open(self._file) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if row['date'] != 'report id':
                    self._data.append((
                        row['employee id'],
                        datetime.strptime(row['date'], '%d/%m/%Y'),
                        row['hours worked'],
                        row['job group']
                    ))
                else:
                    report_id = row['hours worked']

        return report_id

    def _persist_data(self, report_id):
        try:
            self._db_util.populate_payroll(self._data)
            return True
        except RuntimeError:
            self._db_util.delete_report(report_id)
            return False
        finally:
            self._data.clear()

    def process(self):
        report_id = self._read_csv()

        if self._db_util.report_exists(report_id):
            raise ValueError('Report Id already exists')

        try:
            self._db_util.persist_report(report_id)
            return self._persist_data(report_id)
        except RuntimeError:
            return False