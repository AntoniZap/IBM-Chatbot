FROM ubuntu
RUN apt-get -y update ; apt-get -y install git python3 python3-pip
RUN python3 -m pip install --user flake8 pytest
RUN python3 -m pip install --user torch --index-url https://download.pytorch.org/whl/cpu
WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install --user -r requirements.txt
COPY . .
ENTRYPOINT ["python3", "app.py"]
