class Meal:
  def __init__(self, id: str, name: str, description: str, datetime: str, diet=False) -> None:
    self.id = id
    self.name = name
    self.description = description
    self.datetime = datetime
    self.diet = diet
  
  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "description": self.description,
      "datetime": self.datetime,
      "diet": self.diet
    }