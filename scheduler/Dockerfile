FROM python:3.9
ADD ./scheduler /scheduler
WORKDIR /scheduler
RUN pip install -r requirements.txt
ENTRYPOINT ["python","main.py"]
