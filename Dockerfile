FROM python:3
RUN mkdir /flaskerize
#COPY . /flaskerize
COPY requirements.txt /flaskerize
COPY app.py /flaskerize
COPY static /flaskerize/static
COPY templates /flaskerize/templates
WORKDIR /flaskerize
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["app.py"]
