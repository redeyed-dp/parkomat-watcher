import json
import requests
from datetime import datetime

from core.AESCipher import AESCipher
from core.adapters.printer.online_printer.database import Database
from core.checks_and_logs_db import ChecksAndLogsDatabase
from core.configs import MonitoringServerConfig, PrinterConfig
from core.database import Database as CoreDatabase


date = "0921"


def prepare_checks(day="20210325"):
    fn = PrinterConfig().fn
    zn = f'{PrinterConfig().zn_prefix}{MonitoringServerConfig().serial}'
    checks = {
        "checks": [],
        "z_reports": [],
        "incassation_checks": []
    }
    park_checks = tax_db.get_all_checks()
    z_reports = tax_db.get_all_reports()
    incassation_checks = tax_db.get_all_service_checks()
    for check in park_checks:
        if datetime.strptime(check["timestamp"], "%Y%m%d%H%M%S").strftime("%Y%m%d") == day:
            checks["checks"].append({
                "number": check["fiscal_number"],
                "fn": fn,
                "zn": zn,
                "di": check["di"],
                "form_of_payment": check["pay_type"],
                "amount": check["amount"],
                "date": datetime.strptime(check["timestamp"], "%Y%m%d%H%M%S").strftime("%d.%m.%Y %H:%M:%S")
            })
    for report in z_reports:
        if datetime.strptime(report["timestamp"], "%Y%m%d%H%M%S").strftime("%Y%m%d") == day:
            checks["z_reports"].append({
                "number": report["number"],
                "fn": fn,
                "zn": zn,
                "di": report["di"],
                "date": datetime.strptime(report["timestamp"], "%Y%m%d%H%M%S").strftime("%d.%m.%Y %H:%M:%S"),
                "amount": report["cash_amount"] + report["card_amount"],
                "cash": report["cash_amount"],
                "card": report["card_amount"],
                "incassation_check_amount": report["encashment_amount"]
            })
    for check in incassation_checks:
        if datetime.strptime(check["timestamp"], "%Y%m%d%H%M%S").strftime("%Y%m%d") == day:
            checks["incassation_checks"].append({
                "amount": check["amount"],
                "date": datetime.strptime(check["timestamp"], "%Y%m%d%H%M%S").strftime("%d.%m.%Y %H:%M:%S"),
                "fn": fn,
                "zn": zn,
                "di": check["di"]
            })
    checks_and_logs_db.add_day_check_entry(json.dumps({"checks": checks}))

if date and len(date) == 4:
    tax_db = Database()
    tax_db.connect()
    checks_and_logs_db = ChecksAndLogsDatabase()
    checks_and_logs_db.connect()
    settings_db = CoreDatabase()
    settings = settings_db.read_settings()

    for day in range(1, 30):
        prepare_checks(f"202106{str(day).zfill(2)}")

    for day in range(1, 31):
        prepare_checks(f"202107{str(day).zfill(2)}")

    for day in range(1, 31):
        prepare_checks(f"202108{str(day).zfill(2)}")

    if date[0] == "0":
        for day in range(1, int(date[2:])):
            prepare_checks(f"202109{str(day).zfill(2)}")
    else:
        for day in range(1, 31):
            prepare_checks(f"202109{str(day).zfill(2)}")
        if date[1] == "0":
            for day in range(1, int(date[2:])):
                prepare_checks(f"202110{str(day).zfill(2)}")
        if date[1] == "1":
            for day in range(1, 32):
                prepare_checks(f"202110{str(day).zfill(2)}")
            for day in range(1, int(date[2:])):
                prepare_checks(f"202111{str(day).zfill(2)}")
        else:
            for day in range(1, 32):
                prepare_checks(f"202110{str(day).zfill(2)}")
            for day in range(1, 31):
                prepare_checks(f"202111{str(day).zfill(2)}")
            for day in range(1, int(date[2:])):
                prepare_checks(f"202112{str(day).zfill(2)}")

    aesc = AESCipher(settings["private_key"])
    serial_number = settings["serial"]

    check_logs = checks_and_logs_db.get_new_day_check_entries()
    if check_logs:
        for check_log in check_logs:
            print(check_log)
            encrypted = aesc.encrypt(check_log["json_data"])
            response = requests.post(url=f"https://parking-monitoring.icity.com.ua/api/v1/park/{serial_number}/", data=encrypted, timeout=30, headers={'content-type': 'text/plain'})
            print(response)
            if response.status_code == 200:
                checks_and_logs_db.finish_day_check_entry_by_id(check_log["id"])
    else:
        print("Empty DB")
else:
    print("Wrong date")
