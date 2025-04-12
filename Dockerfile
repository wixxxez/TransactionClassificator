FROM python:3.12.7

 
COPY . ./
ENV TZ=Europe/Kiev

RUN pip install -r requirements.txt  

CMD ["python3", "-m", "src.bot.app"]

EXPOSE 8000
 