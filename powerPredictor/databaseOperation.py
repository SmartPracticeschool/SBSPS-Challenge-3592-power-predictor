from powerPredictor import db

class Operation:
    def addEntryToDatabase(entry):
        # this function resturns the response code
        db.session.add(entry)
        try:
            db.session.commit()
        except:
            return 503 
        return 200