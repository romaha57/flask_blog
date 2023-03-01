FROM python

COPY . .

WORKDIR .

RUN pip install -r requirements.txt

CMD ["flask db init"]
CMD ["flask db migrate"]
CMD ["flask db upgrade"]
CMD ["python", "app.py"]