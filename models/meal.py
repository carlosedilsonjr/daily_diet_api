from database import db
from sqlalchemy.orm import Mapped, mapped_column

class Meal(db.Model):
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
  name: Mapped[str] = mapped_column()
  description: Mapped[str] = mapped_column(nullable=True)
  datetime: Mapped[str] = mapped_column()
  diet: Mapped[bool] = mapped_column(default=False)

  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "description": self.description,
      "datetime": self.datetime,
      "diet": self.diet
    }