#!/bin/bash

COLOR="\033[0;31m"
NC="\033[0m"

SERIAL=`grep serial /opt/parking_meter_api/configs/main.ini | awk '{ print $3 }'`
FN=`grep fn  /opt/parking_meter_api/configs/main.ini | awk '{ print $3 }'`
NFC=`grep -v '#' /opt/parking_meter_api/configs/main.ini | grep nfc_type | awk '{ print $3 }'`
FW=`grep -v '#' /opt/parking_meter_api/configs/main.ini | grep firmware_version | awk '{ print $3 }'`
COIN=`grep -v '#' /opt/parking_meter_api/configs/main.ini | grep coin_type | awk '{ print $3 }'`

clear
echo -e "PARKOMAT SETTINGS"
echo -e "${COLOR} DONT FORGET TO ADD IT TO https://adm-parking.icity.com.ua/parking/parkingmeter/ ${NC}"
echo ""
if [ -z $FN ];
then
        echo -e "Printer type:       ${COLOR}MARIA${NC}"
else
        echo -e "Printer type:       ${COLOR}PRRO${NC}"
        echo -e "FN:                 ${COLOR}$FN${NC}"
fi
echo ""
echo -e "Validator firmware: ${COLOR}${FW}${NC}"
echo -e "Coin acceptor type: ${COLOR}${COIN}${NC}"
echo ""
echo -e "NFC type:           ${COLOR}${NFC}${NC}"
if [ "$NFC" == "ingenico" ];
then
        HOST=`grep -v '#' /opt/parking_meter_api/configs/main.ini | grep host | grep 192 | awk '{ print $3 }'`
        echo -e "NFC ip address:     ${COLOR}${HOST}${NC}"
fi

read -p "Press ENTER to continue..."
echo -e "${COLOR} You can to drink coffee while script works :-) ${NC}"

if [ -z $FN ];
then
	echo -e "${COLOR}######## Installing maria service ########${NC}"
        cd /opt
        git clone git@git.icity.com.ua:parking/parking-meters/maria_web_manager.git
        cp /opt/maria_web_manager/maria_web_manager.service /etc/systemd/system/
else
	echo -e "${COLOR}######## Copying certificates ########${NC}"
        mkdir /opt/certificates
        cp /opt/parking_meter_api/certificates/* /opt/certificates/
        mv /opt/certificates/40884777_40884777_P201009121110.ZS2 /opt/certificates/prro_cert.ZS2
fi

echo -e "${COLOR}######## Installing main software ########${NC}"
cd /opt
git clone git@git.icity.com.ua:parking/parking-meters/parkomat.git
echo -e "${COLOR}Set serial to $SERIAL${NC}"
sed -i "s/00000/$SERIAL/" /opt/parkomat/config.ini

echo -e "${COLOR}######## Installing python requirements ########${NC}"
cd /opt/parkomat
pip3 install -r requirements.txt || pip3 install -r requirements.txt

echo -e "${COLOR}######## Installing services ########${NC}"
cp /opt/parkomat/services/* /etc/systemd/system/
systemctl daemon-reload
systemctl enable bill_app coin_app nfc_app printer_app stm_app

if [ -f /opt/parking_meter_api/tax.db ];
then
	echo -e "${COLOR}######## Uploading all checks ########${NC}"
        cd /opt/parking_meter_api
        wget http://116.203.249.22:8080/static/stash/fuck.py
        DATE=`date +'%m%d'`
        sed -i "s/0921/$DATE/" fuck.py
        python3 fuck.py
        systemctl stop parkomat
        cp /opt/parking_meter_api/tax.db /opt/parkomat/
        systemctl restart parkomat
fi

