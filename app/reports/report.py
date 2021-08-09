from app import db
from app.catalog.models import Parkomat
from app.health.models import Health
from sqlalchemy import and_
from datetime import datetime, timedelta
import fpdf

#############################################################################################
#                                  WARNING!!!                                               #
# Don't forget download unicode fonts for FPDF                                              #
# https://github.com/reingart/pyfpdf/releases/download/binary/fpdf_unicode_font_pack.zip    #
#                                                                                           #
#############################################################################################

def morning_report(name):
    offline = []
    status = dict()
    parkomats = Parkomat.observed()
    old = datetime.now() - timedelta(minutes=30)
    for p in parkomats:
        # Офлайн - не выходили на связь более 30 минут
        count = db.session.query(Health).filter(and_(Health.host == p, Health.received > old)).count()
        if count == 0:
            offline.append(str(p))
        else:
            # Состояние ПО
            lastprobe = db.session.query(Health.api).filter(Health.host == p).order_by(Health.id.desc()).first()
            if lastprobe.api != 'ok':
                status[p]['api'] = lastprobe.api
            c = db.session.query(Health).filter(and_(Health.host == p, Health.probed > old, Health.coin == False)).count()
            if c > 10:
                status[p]['coin'] = 'ERROR'
            else:
                status[p]['coin'] = 'OK'
            v =  db.session.query(Health).filter(and_(Health.host == p, Health.probed > old, Health.coin == False)).count()
            if v > 10:
                status[p]['validator'] = 'ERROR'
            else:
                status[p]['validator'] = 'OK'

    pdf = fpdf.FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', '../font/DejaVuSerifCondensed.ttf', uni=True)
    # Head
    pdf.set_font('DejaVu', '', 16)
    d = datetime.now()
    pdf.cell(200, 10, name, 0, 1, "C")
    # Offline
    pdf.set_font('DejaVu', '', 14)
    if len(offline) > 0:
        pdf.cell(200, 10, 'Не выходят на связь более 30 минут:', 0, 1, "C")
        pdf.set_font('DejaVu', '', 12)
        pdf.cell(200, 10, ', '.join(offline), 0, 1, "C")
    else:
        pdf.cell(200, 10, 'Все наблюдаемые паркоматы вышли на связь.', 0, 1, "C")
    # API, devices
    w = pdf.w / 13
    h = pdf.font_size * 1.4
    pdf.set_font('DejaVu', '', 12)
    pdf.multi_cell(w * 2, h, "Паркомат №", 1, 0, 'C')
    pdf.multi_cell(w, h, "Монетник", 1, 0, 'C')
    pdf.multi_cell(w, h, "Купюрник", 1, 0, 'C')
    pdf.multi_cell(w * 8, h, "API", 1, 0, 'C')
    pdf.ln(h)
    for p in status.keys():
        if status[p]['api'] != 'ok' or status[p]['coin'] != 'OK' or status[p]['validator'] != 'OK':
            pdf.multi_cell(w * 2, h, str(p), 1, 0, 'R')
            pdf.multi_cell(w, h, status[p]['coin'], 1, 0, 'C')
            pdf.multi_cell(w, h, status[p]['validator'], 1, 0, 'C')
            pdf.multi_cell(w * 8, h, str(status[p]['API']), 1, 0, 'L')
            pdf.ln(h)
    # footer
    pdf.set_font('DejaVu', '', 8)
    pdf.cell(200, 10, f"Документ сформирован в {str.zfill(str(d.hour), 2)}:{str.zfill(str(d.minute), 2)}:{str.zfill(str(d.second), 2)}", 0, 1, "L")
    pdf.output(f"app/static/reports/{name}.pdf")


def evening_report(name):
    d = datetime.now()
    observed = Parkomat.observed()
    usb = dict()
    drive = []
    for p in observed:
        health = Health.dayStat(host=p, year=d.year, month=d.month, day=d.day)
        usb[p] = Health.counters(health)
        hdd = False
        for h in health:
            if h.hdd == 0:
                hdd = True
        if hdd:
            drive.append(str(p))

    pdf = fpdf.FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', '../font/DejaVuSerifCondensed.ttf', uni=True)
    # Head
    pdf.set_font('DejaVu', '', 16)
    pdf.cell(200, 10, name, 0, 1, "C")
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
    # footer
    pdf.set_font('DejaVu', '', 8)
    pdf.cell(200, 10, f"Документ сформирован в {str.zfill(str(d.hour), 2)}:{str.zfill(str(d.minute), 2)}:{str.zfill(str(d.second), 2)}", 0, 1, "L")
    pdf.output(f"app/static/reports/{name}.pdf")
