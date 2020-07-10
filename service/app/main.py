from flask import Flask, abort, Response, request
from models import db
from models.table import Company, Tag, TagEnum
import config
import csv
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.alchemy_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/', methods=['GET'])
def index():
	return 'Hello World!'

@app.route('/bulk_add', methods=['GET'])
def bulk_add():
	with open('./wanted_temp_data.csv', encoding='utf-8') as f:
		reader = csv.DictReader(f)
		tags = {
			"ko": [],
			"en": [],
			"ja": []
		}
		for row in reader:
			attrs = dict(row.items())
			db.session.add(Company(**attrs))
			tag_ko = attrs['tag_ko'].split('|')
			if tag_ko:
				tags["ko"].extend([tag for tag in tag_ko])
			tag_en = attrs['tag_en'].split('|')
			if tag_en:
				tags["en"].extend([tag for tag in tag_en])
			tag_ja = attrs['tag_ja'].split('|')
			if tag_ja:
				tags["ja"].extend([tag for tag in tag_ja])
			
	for lang, names in tags.items():
		names = list(set(names))
		for name in names:
			attrs = {"name": name, "lang": lang}
			db.session.add(Tag(**attrs))
	db.session.commit()
	return Response(status=201)

@app.route('/company/<int:id>', methods=['GET'])
def get_company(id):
	company = Company.query.get(id)
	if not company:
		res = json.dumps({"msg": "해당하는 회사가 없습니다."}, ensure_ascii=False, indent=4)
		return Response(res, status=404)

	res = json.dumps(company.dumps(), ensure_ascii=False, indent=4)
	return Response(res, status=200)

@app.route('/auto_complete', methods=['GET'])
def auto_complete():
	query = request.args.get('q', '')
	if not query:
		res = json.dumps({"msg": "텍스트를 입력해주세요."}, ensure_ascii=False, indent=4)
		return Response(res, status=400)

	companies = Company.query.filter(
		(Company.name_ko.contains(query)) | 
		(Company.name_en.contains(query)) | 
		(Company.name_ja.contains(query))
	)

	if companies.first() is None:
		res = json.dumps({"msg": "해당하는 회사가 없습니다."}, ensure_ascii=False, indent=4)
		return Response(res, status=404)

	res = json.dumps([c.dumps() for c in companies], ensure_ascii=False, indent=4)
	return Response(res, status=200)

@app.route('/search', methods=['GET'])
def search():
	query = request.args.get('tag', '')
	tag = Tag.query.filter_by(name=query).first()
	if tag is None:
		res = json.dumps({"msg": "해당하는 회사가 없습니다."}, ensure_ascii=False, indent=4)
		return Response(res, status=404)

	companies = Company.query.filter(
		(Company.tag_ko.contains(tag.name)) | 
		(Company.tag_en.contains(tag.name)) | 
		(Company.tag_ja.contains(tag.name))
	)

	res = json.dumps([c.dumps() for c in companies], ensure_ascii=False, indent=4)
	return Response(res, status=200)

@app.route('/add_tag/<int:id>', methods=['PUT'])
def add_tag(id):
	data = request.json
	tag = data.get('tag')
	lang = data.get('lang')
	if tag is None or tag == "":
		res = json.dumps({"msg": "추가할 태그를 입력해주세요"}, ensure_ascii=False, indent=4)
		return Response(res, status=400)
	if lang not in ['ko', 'en', 'ja']:
		res = json.dumps({"msg": "태그의 언어를 정확히 입력해주세요"}, ensure_ascii=False, indent=4)
		return Response(res, status=400)
	
	company = Company.query.get(id)
	res = company.dumps()
	tags = res['tag_{}'.format(lang)].split("|")
	if tag in tags:
		res = json.dumps({"msg": "이미 존재하는 태그입니다."}, ensure_ascii=False, indent=4)
		return Response(res, status=400)

	query = Tag.query.filter_by(name=tag).first()
	if query is None:
		db.session.add(Tag(name=tag, lang=lang))

	tags.append(tag)
	
	if lang == "ko":
		company.tag_ko = "|".join(tags)
	elif lang == "en":
		company.tag_en = "|".join(tags)
	else:
		company.tag_ja = "|".join(tags)
	db.session.commit()

	res = json.dumps(company.dumps(), ensure_ascii=False, indent=4)
	return Response(res, status=200)

@app.route('/del_tag/<int:id>', methods=['PUT'])
def del_tag(id):
	data = request.json
	tag = data.get('tag')
	lang = data.get('lang')
	if tag is None:
		res = json.dumps({"msg": "삭제할 태그를 입력해주세요"}, ensure_ascii=False, indent=4)
		return Response(res, status=400)
	if lang not in ['ko', 'en', 'ja']:
		res = json.dumps({"msg": "태그의 언어를 정확히 입력해주세요"}, ensure_ascii=False, indent=4)
		return Response(res, status=400)
	
	company = Company.query.get(id)
	res = company.dumps()
	tags = res['tag_{}'.format(lang)].split("|")
	if tag not in tags:
		res = json.dumps({"msg": "존재하지 않는 태그입니다."}, ensure_ascii=False, indent=4)
		return Response(res, status=400)
	tags.remove(tag)
	
	if lang == "ko":
		company.tag_ko = "|".join(tags)
	elif lang == "en":
		company.tag_en = "|".join(tags)
	else:
		company.tag_ja = "|".join(tags)
	db.session.commit()

	res = json.dumps(company.dumps(), ensure_ascii=False, indent=4)
	return Response(res, status=200)


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=5000)
	
