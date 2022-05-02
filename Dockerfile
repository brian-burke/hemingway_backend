# start by pulling the python image
FROM python:3.8-alpine

RUN apk update && apk add python3-dev \
                          gcc \
                          libc-dev \
                          libffi-dev

# copy the requirements file into the image
COPY api/requirements.txt /code/requirements.txt

# switch working directory
WORKDIR /code

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /code

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0","--port=7007"]