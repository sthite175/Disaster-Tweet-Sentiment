FROM python:3.10

COPY . /home
WORKDIR /home

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Download all NLTK data
RUN python -c "import nltk; nltk.download('all')"

EXPOSE 8888 

CMD  ["python", "app.py"]