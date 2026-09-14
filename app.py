import os
from datetime import datetime, timezone

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# подгружаем переменные из .env
load_dotenv()

app = Flask(__name__)

# собираем строку подключения из переменных окружения
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

db = SQLAlchemy(app)


# модель Visit: id, время обращения, IP клиента
class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visit_time = db.Column(db.DateTime(timezone=True), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)


# создаём таблицу visits при старте приложения
with app.app_context():
    db.create_all()


# маршрут GET /hello
@app.get("/hello")
def hello():
    # формируем запись: текущее время + IP клиента
    visit = Visit(
        visit_time=datetime.now(timezone.utc),
        ip_address=request.remote_addr or "unknown"
    )

    # сохраняем в БД
    db.session.add(visit)
    db.session.commit()

    return "Hello", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)