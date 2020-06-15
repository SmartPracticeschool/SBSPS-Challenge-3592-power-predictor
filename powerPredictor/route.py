import bcrypt
from flask import request
from powerPredictor import app
from powerPredictor.models import User, PowerPlant
from powerPredictor.response import Response 
from powerPredictor.databaseOperation import Operation
from powerPredictor.otp import Otp, otpSender

'''
Response code:
400 -> Bad request, something wrong with parameters
409 -> resourse already exist, User/PowerPlant already exist
200 -> OK, Intended task completed
404 -> NO data found
503 -> Error in database, unable to enter data into table
401 -> not authorised, Wrong password/otp
502 -> Unable to send mail, something wrong with mail id
'''


'''
Parameters:
name -> userName
email -> user email
password -> password
'''
@app.route('/signup', methods=['POST'])
def signUp():
   userName = request.args.get('name')
   userEmail = request.args.get('email')
   userPassword = request.args.get('password')

   if userName and userEmail and userPassword:
      user=User.query.filter_by(email=userEmail).first()
      if not user:
         hashedPasswor = bcrypt.hashpw(userPassword.encode('utf-8'), bcrypt.gensalt())
         user=User(name=userName, email=userEmail, password=hashedPasswor)
         statusCode=Operation.addEntryToDatabase(user)
         return Response.createResponseFromStatus(statusCode)
      return Response.createResponseFromStatus(409)
   return Response.createResponseFromStatus(400)


@app.route('/resendotp', methods=['POST'])
def ResendOtp():
   statusCode=otpSender.reSendCode()
   return Response.createResponseFromStatus(statusCode)

'''
parameters:
otp -> user entered otp
'''
@app.route('/checkotp', methods=['POST'])
def CheckOtp():
   otp = request.args.get('otp')
   if otp:
      otpResponse=otpSender.checkOTP(otp)
      if otpResponse==404:
         return Response.createResponseFromStatus(otpResponse)
      elif otpResponse:
         user=otpSender.user
         statusCode=Operation.addEntryToDatabase(user)
         otpSender.user=None
         return Response.createResponseFromStatus(statusCode)
      return Response.createResponseFromStatus(401)
   return Response.createResponseFromStatus(400)

@app.route('/database', methods=['GET'])
def viewDatabase():
   users= User.query.all()
   if users:
      return Response.getDatabase(users)
   return Response.createResponseFromStatus(404)


'''
parameters:
email -> email of the user
password -> password of the user
'''

@app.route('/login', methods=['PUT'])
def Login():
   userEmail = request.args.get('email')
   userPassword = request.args.get('password')
   if userEmail and userPassword:
      user=User.query.filter_by(email=userEmail).first()
      if user:
         if bcrypt.checkpw(userPassword.encode('utf-8'), user.password):
            return Response.getDetalisOf(user)
         return Response.createResponseFromStatus(401)
      return Response.createResponseFromStatus(404)
   return Response.createResponseFromStatus(400)   
