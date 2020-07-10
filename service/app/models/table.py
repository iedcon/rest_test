from models import db
import enum
from datetime import datetime

class Company(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name_ko = db.Column(db.String(30))
	name_en = db.Column(db.String(30))
	name_ja = db.Column(db.String(30))
	tag_ko = db.Column(db.Text)
	tag_en = db.Column(db.Text)
	tag_ja = db.Column(db.Text)

	def dumps(self):
		res = {
			'id': self.id,
			'name_ko': self.name_ko,
			'name_en': self.name_en,
			'name_ja': self.name_ja,
			'tag_ko': self.tag_ko,
			'tag_en': self.tag_en,
			'tag_ja': self.name_ja
		}
		return res


class TagEnum(enum.Enum):
	ko = 'ko'
	en = 'en'
	ja = 'ja'


class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False, unique=True)
	lang = db.Column(db.Enum(TagEnum), default=TagEnum.ko, nullable=False)
