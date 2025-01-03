FROM python:3.12

WORKDIR /app

COPY requirements.txt ./

RUN mkdir requirements

COPY requirements/prod.txt requirements/common.txt requirements/

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-m", "src.app", "run" ]
