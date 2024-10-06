FROM python

WORKDIR /Users/Nizar/OneDrive - Hogeschool Rotterdam/secure-wp3/

COPY requirements.txt ./
RUN pip install blinker
RUN pip install cffi
RUN pip install click
RUN pip install colorama
RUN pip install cryptography
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
RUN pip install python-dotenv



COPY . .

CMD [ "python", "main.py"]
EXPOSE 5000