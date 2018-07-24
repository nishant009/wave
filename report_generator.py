import pydash as _

from calendar import monthrange
from db_util import DBUtil

class ReportGenerator(object):
    _DATE_INDEX = 0
    _EID_INDEX = 1
    _HOURS_INDEX = 2
    _JOB_GROUP_INDEX = 3

    def __init__(self, db_util):
        if _.is_empty(db_util) or not isinstance(db_util, DBUtil):
            raise RuntimeError('DB Util object missing or invalid. Please provide a valid util.')
        
        self._db_util = db_util

    def generate_report(self):
        res = {}
        data = self._db_util.get_report_data()

        for row in data:
            date = row[self._DATE_INDEX]
            employee_id = row[self._EID_INDEX]
            job_group = row[self._JOB_GROUP_INDEX]
            
            last_day = monthrange(date.year, date.month)

            rate = 20 if job_group == 'A' else 30

            if date.day < 15:
                key = '15' + str(date.month) + str(date.year)
                period = '1/' + str(date.month) + '/' + str(date.year) + '-' + '15/' + str(date.month) + '/' + str(date.year)
            else:
                key = str(last_day[1]) + str(date.month) + str(date.year)
                period = '16/' + str(date.month) + '/' + str(date.year) + '-' + str(last_day[1]) + '/' + str(date.month) + '/' + str(date.year)

            if key not in res.keys():
                res[key] = {}
            
            if employee_id not in res[key].keys():
                res[key][employee_id] = {
                    'period': period,
                    'hours': row[self._HOURS_INDEX],
                    'rate': rate
                }
            else:
                res[key][employee_id]['hours'] += row[self._HOURS_INDEX]
        
        return res
