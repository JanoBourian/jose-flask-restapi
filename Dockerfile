FROM python:3.11
ENV FLASK_APP main.py
EXPOSE 5000
WORKDIR /code
COPY . .
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
CMD ["flask", "run", "--host", "0.0.0.0"]