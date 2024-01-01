FROM continuumio/miniconda3:latest

COPY . /home
WORKDIR /home

# If you need to upgrade pip, you can uncomment the following line
RUN pip install --upgrade pip

# Add channels
RUN conda config --add channels conda-forge
RUN conda config --add channels defaults

RUN conda install --file requirements.txt

EXPOSE 8888

CMD ["python", "app.py"]

