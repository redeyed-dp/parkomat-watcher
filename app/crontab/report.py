from app import db
from app.catalog.models import Parkomat
from app.health.models import Health
from app.lib.telegram import tg_send_message, tg_send_file
from sqlalchemy import and_
from datetime import datetime, timedelta
import fpdf

def morning_report():
    offline = []
    api = []
    parkomats = Parkomat.observed()
    old = datetime.today() - timedelta(minutes=30)
    for p in parkomats:
        count = db.session.query(Health).filter(and_(Health.host == p, Health.received > old)).count()
        if count == 0:
            offline.append(p)
        else:
            lastprobe = db.session.query(Health.api).filter(Health.host == p).order_by(Health.id.desc()).first()
            if lastprobe.api != 'ok':
                api.append("№{}: {}\n".format(p, lastprobe.api))
    if len(offline) > 0:
        tg_send_message("Не вышли на связь: {}".format(', '.join(offline)))
    if len(api) > 0:
        tg_send_message("Проблемы API: \n {}".format("\n".join(api)))
    if len(offline) == 0 and len(api) == 0:
        tg_send_message("На всех наблюдаемых паркоматах все ОК :-)")

def evening_report():
    d = datetime.now()
    observed = Parkomat.observed()
    usb = dict()
    hdd = dict()
    for p in observed:
        health = Health.dayStat(host=p, year=d.year, month=d.month, day=d.day)
        usb[p] = Health.counters(health)
        for h in health:
            if h.hdd == 0:
                hdd[p] = True
    drive = hdd.keys()

    pdf = fpdf.FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', '../font/DejaVuSerifCondensed.ttf', uni=True)
    # Head
    pdf.set_font('DejaVu', '', 16)
    pdf.cell(200, 10, f"Отчет {d.day}.{d.month}.{d.year}", 0, 1, "C")
    # Drive errors
    pdf.set_font('DejaVu', '', 14)
    pdf.cell(200, 10, '"Отпадания" накопителя', 0, 1, "C")
    pdf.set_font('DejaVu', '', 12)
    if len(drive) == 0:
        pdf.cell(200, 10, "Отпаданий жесткого диска не обнаружено", 0, 1, "L")
    else:
        pdf.cell(200, 10, ', '.join(drive), 0, 1, "L")
    # USB errors and reboots
    pdf.set_font('DejaVu', '', 14)
    pdf.cell(200, 10, '"Отпадания" USB устройств', 0, 1, "C")
    w = pdf.w / 6.5
    h = pdf.font_size * 1.4
    pdf.set_font('DejaVu', '', 12)
    pdf.cell(w, h, "Паркомат №", 1, 0, 'C')
    pdf.cell(w, h, "Монетник", 1, 0, 'C')
    pdf.cell(w, h, "Купюрник", 1, 0, 'C')
    pdf.cell(w, h, "Принтер", 1, 0, 'C')
    pdf.cell(w, h, "NFC Exellio", 1, 0, 'C')
    pdf.cell(w, h, "Перезагрузки", 1, 0, 'C')
    pdf.ln(h)
    for p in usb.keys():
        pdf.cell(w, h, str(p), 1, 0, 'R')
        pdf.cell(w, h, str(usb[p]['coin']), 1, 0, 'C')
        pdf.cell(w, h, str(usb[p]['validator']), 1, 0, 'C')
        pdf.cell(w, h, str(usb[p]['nfc']), 1, 0, 'C')
        pdf.cell(w, h, str(usb[p]['printer']), 1, 0, 'C')
        pdf.cell(w, h, str(usb[p]['reboot']), 1, 0, 'C')
        pdf.ln(h)
    pdf.output(f"report {d.day}-{d.month}-{d.year}.pdf")
    tg_send_file(f"report {d.day}-{d.month}-{d.year}.pdf")