from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    """Representa un marco o lente."""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), nullable=False)  # 'frame' o 'lens'
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50))
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    # Atributos específicos
    color = db.Column(db.String(30))
    material = db.Column(db.String(50))      # acetato, metal, titanio...
    style = db.Column(db.String(30))         # moderno, clásico, retro...
    features = db.Column(db.String(100))     # "Blue Light, Polarized" (para lentes)
    stock = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Announcement(db.Model):
    """Operativos, eventos o anuncios."""
    __tablename__ = 'announcements'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(200))
    image_url = db.Column(db.String(255))
    is_featured = db.Column(db.Boolean, default=False)
    is_past = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)