from flask import request
from powerPredictor import app
from powerPredictor.models import User, PowerPlant
from powerPredictor.response import Response 
from powerPredictor.databaseOperation import Operation

'''
Response code:
400 -> Bad request, something wrong with parameters
409 -> resourse already exist, User/PowerPlant already exist
200 -> OK, Intended task completed
404 -> NO data found
503 -> Error in database, unable to enter data into table
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
         user=User(name=userName, email=userEmail, password=userPassword)
         statusCode=Operation.addEntryToDatabase(user)
         return Response.createResponseFromStatus(statusCode)
      return Response.createResponseFromStatus(409)
   return Response.createResponseFromStatus(400)


@app.route('/database', methods=['GET'])
def viewDatabase():
   users= User.query.all()
   if users:
      return Response.getDatabase(users)
   return Response.createResponseFromStatus(404)
   