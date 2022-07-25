import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

import pytest

sender_receiver_pair = dict()

def main():
	secret_santa_players_email = list()
	secret_santa_players_name = list()
	gift_receiver_candidates = list()

	exclude_list = dict()

	with open("emails.txt", "r") as email_file:
		for email in email_file:
			email = email.strip()
			secret_santa_players_email.append(email)
	
	with open("names.txt", "r") as name_file:
		for name in name_file:
			name = name.strip()
			secret_santa_players_name.append(name)
	
	excludes = list()

	for name in secret_santa_players_name:
		print(f"Exclude list for {name}")
		
		for (i, name2) in enumerate(secret_santa_players_name):
			print(f"{i}. {name2}")

		excludes = input("Enter the number, seperate it with comma to add multiple name to the list\n> ")
		exclude_list[name] = excludes.replace(" ", "").split(",")


	gift_receiver_candidates = getSecretSantaList(secret_santa_players_name, exclude_list)

	send_secret_santa_email(secret_santa_players_email, gift_receiver_candidates)

def getSecretSantaList(sender_candidates = [], exclude_list = {}):
	received_gift_member_list = list()
	gift_receiver_list = list()

	for (i, name) in enumerate(sender_candidates):
		candidates = sender_candidates.copy()
		candidates.remove(name)
		for excluded_name_index in exclude_list[name]:
			candidates.remove(sender_candidates[int(excluded_name_index)])

		if (len(received_gift_member_list) > 0):
			for excluded_name in received_gift_member_list:
				if (candidates.count(excluded_name) == 0):
					continue

				candidates.remove(excluded_name)

		rand_index = random.randint(0, len(candidates) - 1)
		# print(f"{len(candidates)} - {rand_index}")
		received_gift_member_list.append(candidates[rand_index])

		gift_receiver_list.append(candidates[rand_index])
	
	return gift_receiver_list

def send_secret_santa_email(gift_sender_emails = [], gift_receiver_emails = []):
	port = 465
	password = "SECRET"

	context = ssl.create_default_context()

	sender_email = "SECRET"
	text = "test"
	html = """
<html>
  <body>
    <h1 style="color: red">Secret Santa Result</h1>
	<p>Your gift receiver: <strong>{receiver}</strong></p>
  </body>
</html>
"""


	with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
		server.login(sender_email, password)
		for (i, email) in enumerate(gift_sender_emails):
			message = MIMEMultipart("alternative")
			message["Subject"] = "Bryan Secret Santa Test"
			message["From"] = sender_email
			message["To"] = email

			html_text = MIMEText(html, "html")

			message.attach(html_text)

			server.sendmail(sender_email, email, message.as_string().format(receiver=gift_receiver_emails[i]))


	


if __name__ == "__main__":
	main()

		