FROM python

WORKDIR /herkansing-security-Nizar1012373/werkplaats-3---inhaalopdracht-Nizar-1012373

COPY requirements.txt ./
RUN pip install blinker
RUN pip install click
RUN pip install colorama
RUN pip install Flask
RUN pip install Flask-IPFilter
RUN pip install Flask-SQLAlchemy
RUN pip install greenlet
RUN pip install itsdangerous
RUN pip install Jinja2
RUN pip install MarkupSafe
RUN pip install SQLAlchemy
RUN pip install typing_extensions
RUN pip install Werkzeug



COPY . .

CMD [ "python", "./main.py"]
EXPOSE 5000