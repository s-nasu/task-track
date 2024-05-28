FROM python:3.12
WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN apt update

EXPOSE 8000

# アプリケーションの起動コマンド
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
