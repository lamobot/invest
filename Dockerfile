FROM python:3.8.5

WORKDIR /script
COPY requirements.txt .
RUN pip install -i https://test.pypi.org/simple/ \
    --extra-index-url=https://pypi.org/simple/ tinkoff-invest-openapi-client && \
    pip install -r requirements.txt
COPY main.py /script/
ENTRYPOINT [ "python", "./main.py" ]
