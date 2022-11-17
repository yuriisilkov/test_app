FROM python:3.9
WORKDIR /git-test

COPY . .

RUN apt-get update && apt-get install -y wget

RUN pip install -r requirements.txt

CMD ["python3", "-m", "nose", "tests/test_api.py"]
