class Response:
    
    STATUS = 'status'
    DATABASE = 'database'
    NAME='name'
    EMAIL='email'
    POWERPLANT='powerPlant'

    def createResponseFromStatus(code):
        return {Response.STATUS: code}
    
    def getDatabase(users):
        database=[]
        for user in users:
            userData={Response.NAME: user.name, Response.EMAIL: user.email}
            powerPlants=user.powerPlants
            powerPlantsData=[]
            for powerPlant in powerPlants:
                powerPlantDict = {Response.NAME: powerPlant.name}
                powerPlantsData.append(powerPlantDict)
            userData[Response.POWERPLANT] = powerPlantsData
            database.append(userData)
        return {Response.DATABASE: database}
        
            