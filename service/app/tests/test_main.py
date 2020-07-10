import sys
import os
import json
import time
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from main import app 

client = app.test_client()

headers = {'Content-Type': 'application/json'}

def test_index():
	response = client.get('/')
	assert response.status_code == 200

def test_auto_complete():
	response = client.get('/auto_complete?q=want')
	assert response.status_code == 200

def test_auto_complete_fail():
	response = client.get('/auto_complete?q=wantsdfsdfdsf')
	assert response.status_code == 404

def test_search():
	response = client.get('/search?tag=tag_4')
	assert response.status_code == 200

def test_search_fail():
	response = client.get('/search?tag=want')
	assert response.status_code == 404

def test_add_tag():
	response = client.put('/add_tag/1', data=json.dumps({"tag": "태그_99", "lang": "ko"}), headers=headers)
	assert response.status_code == 200

def test_add_tag_exists():
	response = client.put('/add_tag/1', data=json.dumps({"tag": "태그_99", "lang": "ko"}), headers=headers)
	assert response.status_code == 400

def test_add_tag_none():
	response = client.put('/add_tag/1', data=json.dumps({"lang": "ko"}), headers=headers)
	assert response.status_code == 400

def test_add_tag_empty():
	response = client.put('/add_tag/1', data=json.dumps({"tag": "", "lang": "ko"}), headers=headers)
	assert response.status_code == 400

def test_add_tag_lang():
	response = client.put('/add_tag/1', data=json.dumps({"tag": "태그_99", "lang": "korfs"}), headers=headers)
	assert response.status_code == 400

def test_del_tag():
	response = client.put('/del_tag/1', data=json.dumps({"tag": "태그_99", "lang": "ko"}), headers=headers)
	assert response.status_code == 200

def test_del_tag_non_exist():
	response = client.put('/del_tag/1', data=json.dumps({"tag": "태그_99", "lang": "ko"}), headers=headers)
	assert response.status_code == 400

def test_del_tag_none():
	response = client.put('/del_tag/1', data=json.dumps({"lang": "ko"}), headers=headers)
	assert response.status_code == 400

def test_del_tag_empty():
	response = client.put('/del_tag/1', data=json.dumps({"tag": "", "lang": "ko"}), headers=headers)
	assert response.status_code == 400

def test_del_tag_lang():
	response = client.put('/del_tag/1', data=json.dumps({"tag": "태그_99", "lang": "korfs"}), headers=headers)
	assert response.status_code == 400

