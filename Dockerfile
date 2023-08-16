FROM ubuntu:latest

RUN apt update 
RUN apt install -y python3 \
     python3-pip 

WORKDIR /app

# copy over requirements in its own Docker layer first:
# we'll only re-download requirements if anything changes
COPY script/requirements.txt /app
RUN pip3 install -r /app/requirements.txt

# and then copy everything else
COPY ./script /app

ENTRYPOINT ["python3"]
CMD ["etl_dropin_ws.py"]
