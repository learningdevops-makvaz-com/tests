FROM selenium/standalone-chrome

COPY . /app

RUN sudo apt update && sudo apt-get -y install python3-pip && pip3 install selenium

ENTRYPOINT ["/app/test.py"]
