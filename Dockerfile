FROM python

WORKDIR /app

COPY main.py requirements.txt ./

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]

EXPOSE 3000
