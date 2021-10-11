FROM python:3.7

RUN apt-get update
COPY requirements.txt requirements.txt  
RUN pip3 install --upgrade pip
RUN pip3 install fastapi uvicorn
RUN pip3 install -r requirements.txt 
COPY ./app /app 
ENV PYTHONPATH "${PYTHONPATH}:/app"   
CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 app.main:app