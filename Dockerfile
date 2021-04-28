FROM python

WORKDIR /app

COPY main.py requirements.txt config.cfg ./

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]

EXPOSE 3000
