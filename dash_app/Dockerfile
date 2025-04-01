#python
FROM python:3.9-slim

WORKDIR /app

#download pips requirements to container from working directry. 
COPY . /app
RUN pip install pandas dash plotly psycopg2-binary irc
#copy files into container. if above installs pip requirements, what does is this copying??? 

#RUN app??? :) example suggests to port orward.
CMD ["python", "DashApper.py"]