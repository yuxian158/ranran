FROM python:3

WORKDIR /ranran

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update \
    && apt-get -y install zip unzip

CMD [ "python", "-m" ,"ranran"]
# CMD [ "ls"]