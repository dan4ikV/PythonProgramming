import smtplib
import argparse
import datetime
import requests
from bs4 import BeautifulSoup


def send_mail(message, credentials_file, subject, receipent):
    if message is not None:
        try:
            with open(credentials_file) as file:
                login, password = file
            smtpSrv = smtplib.SMTP('smtp.gmail.com')
            smtpSrv.starttls()
            smtpSrv.ehlo()
            smtpSrv.login(login, password)
            if subject is None:
                subject = ""
            literal_line = "\\n"
            line = "\n"
            return smtpSrv.sendmail("256711@student.pwr.deu.pl", receipent, f'From: Danylo Vasylyshyn <256711@student.pwr.edu.pl>\nSubject: {subject}({datetime.datetime.today().strftime("%b %d %Y %H:%M:%S")})\n{line.join(message.split(literal_line))}')
        except FileNotFoundError:
            print(f"Invalid credentials file: {credentials_file}")


def parse_arguments():
    parser = argparse.ArgumentParser(description="This app can send mails, parse info from http requests")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-m', '--mail', help="Message to be sent")
    parser.add_argument('-c', '--credentials_file', help="file containing e-mail login credentials (default cred.txt)")
    parser.add_argument('-s', '--subject', help="email's subject")
    parser.add_argument('-r', '--recipient', help="email's recipient")
    group.add_argument('-f', '--cat_facts', help="number of cat facts to get about cats")
    group.add_argument('-t', '--teachers', help="number of cat facts to get about cats")
    args = parser.parse_args()
    if args.credentials_file is None:
        args.credentials_file = "cred.txt"
    if args.recipient is None:
        args.recipient = "wojciech.thomas@pwr.edu.pl"
    return args


def web_scrape_researchers(letter):
    if not letter is None:
        resp = requests.get(f"https://wiz.pwr.edu.pl/pracownicy?letter={letter}")
        soup = BeautifulSoup(resp.text, 'lxml')
        res = []
        print("Web scraping researchers: ")
        for link in soup.findAll('a', {"class": "title"}, href=True):
            res.append({'name': link['title'], 'email': link.find_next_sibling().text[7:]})
        return res
    else:
        return []


def http_request_cat_facts(facts_no):
    if not facts_no is None:
        print('Searching for random cat facts...')
        return requests.get(f'https://cat-fact.herokuapp.com/facts/random?animal_type=cat&amount={facts_no}').json()
    else:
        return []

args = parse_arguments()
send_mail(args.mail, args.credentials_file, args.subject, args.recipient)

for fact in http_request_cat_facts(args.cat_facts):
    print(fact['text'])

for person in web_scrape_researchers(args.teachers):
    print(f"{person['name']}  {person['email']}")