FROM python:3.7-alpine

MAINTAINER anmmscs_mwish@qq.com


RUN pip install -i "https://mirrors.ustc.edu.cn/pypi/web/simple" pipenv

WORKDIR /app

COPY Pipfile.lock Pipfile /app/

RUN pipenv install --system --deploy

ADD . /app

EXPOSE 5000

ENV FLASK_APP app.py

CMD ["python", "app.py"]