import math, random 
import os
from flask_mail import Mail, Message
from powerPredictor import app

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')
mail = Mail(app)

class Otp:
    VARIFICATIONCODE='Varification Code'
    def sendCodeTo(self, user):
        self.user = user
        self.OTP = self.generateOTP()
        msg = Message(self.VARIFICATIONCODE, recipients=[self.user.email])
        msg.body = "Your code :" + self.OTP
        try:
            mail.send(msg)
        except:
            return 502
        return 200
    
    def reSendCode(self):
        if self.user:
            self.OTP = self.generateOTP()
            msg = Message(self.VARIFICATIONCODE, recipients=[self.user.email])
            msg.body = "Your code :" + self.OTP
            try:
                mail.send(msg)
            except Exception as error:
                return 502
            return 200
        return 404
    
    def checkOTP(self, otp):
        if self.OTP:
            didMatched=False
            if otp == self.OTP:
                didMatched=True
            self.OTP=None
            return didMatched
        return 404

    
    def generateOTP(self) :  
        digits = "0123456789"
        OTP = "" 
        for i in range(6) : 
            OTP += digits[math.floor(random.random() * 10)] 
    
        return OTP 

otpSender=Otp()
