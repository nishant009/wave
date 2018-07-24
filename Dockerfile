FROM python:3.6

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . .

EXPOSE 5000

CMD python server.py --host=$HOST --user=$USER --password=$PASSWORD --db=$DB