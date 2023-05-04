FROM python:3.10
EXPOSE 5000
WORKDIR /Festival-Ticket System
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run"]