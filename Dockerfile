FROM python:3.9-alpine
ADD main.py requirements.txt ./
RUN pip install -r requirements.txt
CMD ["python","./main.py"]