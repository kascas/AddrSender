from email.header import Header
from email.mime.text import MIMEText
import os
import smtplib

config_file = '.addr_sender_config'
record_file = '.addr_sender_record'


def get_wlan_setting():
    net_setting = os.popen('ipconfig', 'r')
    wlan_setting_head = '无线局域网适配器 WLAN:\n'
    wlan_setting = dict()
    start_flag, last_key = 0, ''

    for line in net_setting.readlines():
        if line == wlan_setting_head:
            start_flag = 1
            continue
        if start_flag == 0:
            continue
        if line.strip() == '':
            continue
        if line.lstrip() == line:
            break
        item_key = line.split(':')[0].replace('.', '').strip()
        item_value = ':'.join(line.split(':')[1:]).strip()
        if line.count(':') < 1:
            if last_key != '':
                wlan_setting[last_key] = wlan_setting[last_key] + ', ' + line.strip()
            continue
        wlan_setting[item_key] = item_value
        last_key = item_key
    net_setting.close()
    return wlan_setting

def send_email(addr):
    message = MIMEText(addr.encode(), 'plain', 'utf-8')
    subject = 'IP地址更新'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP('smtp.XXX.com')
        smtpObj.starttls()
        smtpObj.login('XXX@XXX.XXX', 'XXX')
        smtpObj.sendmail('XXX@XXX.XXX', 'XXX@XXX.XXX', message.as_string())
    except Exception as e:
        with open(record_file, 'a') as fp:
            fp.write('[Exception]: {}\n'.format(e))

def check_and_send(on_start=False):
    wlan_setting=get_wlan_setting()
    if 'IPv6 地址' not in wlan_setting:
        return False
    last_addr, tmp = '', ''
    current_addr = wlan_setting['IPv6 地址'].strip()
    if not os.path.exists(config_file):
        with open(config_file, 'w') as fp:
            pass
    if not os.path.exists(record_file):
        with open(record_file, 'w') as fp:
            pass
    with open(config_file, 'r') as fp:
        last_addr = fp.read().strip()
    if current_addr == last_addr:
        if on_start:
            send_email(current_addr)
        return True
    else:
        if on_start:
            send_email(current_addr)
        else:
            send_email(current_addr)
        with open(record_file, 'a') as fp:
            fp.write('[Update]: {}\n'.format(current_addr))
    with open(config_file, 'w') as fp:
        fp.write(current_addr)
    with open(record_file, 'r') as fpr:
        tmp=fpr.readlines()[:1000]
    with open(record_file, 'w') as fpw:
        fpw.writelines(tmp)
    return True


if __name__=='__main__':
    check_and_send()
    