import click
from app import app
from datetime import datetime

@app.cli.command("admin")
def create_admin():
    from app import db
    from app.models import Admin
    login = input("Enter login: ")
    name = input("Enter name: ")
    password = input("Enter password: ")
    admin = Admin(login=login, name=name)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    print("New admin created successfully")

@app.cli.command("report")
@click.argument("n")
def report(n):
    d = datetime.now()
    name = f"Отчет {d.year}.{str.zfill(str(d.month), 2)}.{str.zfill(str(d.day), 2)} {str.zfill(str(d.hour), 2)}:{str.zfill(str(d.minute), 2)}"
    if n == "evening":
        name += ' (вечерний)'
        from app.reports.report import evening_report
        evening_report(name)
    elif n =="morning":
        name += ' (утренний)'
        from app.reports.report import morning_report
        morning_report(name)