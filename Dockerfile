FROM python:3.7.7
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
COPY application.py /app/
COPY data.csv /app/
COPY drivedata.csv /app/
COPY forreordering-38e3f0bc72c3.json /app/
COPY import_file.csv /app/
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
EXPOSE 8080
CMD [ "python", "application.py" ]


