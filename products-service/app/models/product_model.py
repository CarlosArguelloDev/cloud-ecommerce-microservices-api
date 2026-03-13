from app import db


class Product(db.Model):
    __tablename__ = "products"

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(120), nullable=False)
    price         = db.Column(db.Float,       nullable=False)
    category      = db.Column(db.String(60),  nullable=False)   # tropical | interior | suculenta | helecho
    image         = db.Column(db.String(200),  nullable=False)   # filename inside public/images/
    care          = db.Column(db.String(200),  nullable=False)
    badge         = db.Column(db.String(40),   nullable=True)    # "Nuevo" | "Popular" | "Exótica" | "-20%" | null
    badge_type    = db.Column(db.String(20),   nullable=True)    # "new" | "sale" | null
    original_price = db.Column(db.Float,       nullable=True)    # shows strikethrough in UI

    def to_dict(self):
        return {
            "id":            self.id,
            "name":          self.name,
            "price":         self.price,
            "category":      self.category,
            "image":         self.image,
            "care":          self.care,
            "badge":         self.badge,
            "badgeType":     self.badge_type,
            "originalPrice": self.original_price,
        }
