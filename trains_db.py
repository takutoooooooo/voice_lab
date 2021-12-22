from server import db

class TrainTable(db.Model):
	TrainId = db.Column(db.Integer, nullable=False, primary_key=True)
	TrainName = db.Column(db.String)
	
	__tablename__ = "train"