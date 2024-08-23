from app import db

class Robot(db.Model):
    __tablename__ = 'robots'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64))
    description = db.Column(db.Text())
    url = db.Column(db.Text())
    credentials = db.Column(db.String(128))
    healthy = db.Column(db.Boolean(),default=True)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def save(self):
      db.session.add(self)
      db.session.commit()
    
    def delete(self):
      db.session.delete(self)
      db.session.commit()


