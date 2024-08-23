from app import db

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(128))
    content = db.Column(db.String(128))

    def save(self):
      db.session.add(self)
      db.session.commit()
    
    def delete(self):
      db.session.delete(self)
      db.session.commit()

class Broken(db.Model):
    __tablename__ = 'broken'
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.Text())

    def save(self):
      db.session.add(self)
      db.session.commit()
    
    def delete(self):
      db.session.delete(self)
      db.session.commit()