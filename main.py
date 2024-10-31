from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

app = Flask(__name__)
driver = None

@app.route('/find_element', methods=['POST'])
def find_element():
    global driver
    data = request.get_json()
    
    # Kiểm tra JSON
    if not data or 'url' not in data or 'element_id' not in data:
        return jsonify({"error": "Invalid JSON data"}), 400

    url = data['url']
    element_id = data['element_id']

    # Sử dụng Service để tạo driver với ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get(url)

    try:
        element = driver.find_element(By.ID, element_id)
        result = element.text
    except Exception as e:
        result = str(e)

    driver.quit()
    return jsonify({"result": result})

@app.route('/open', methods=['GET'])
def open():
    global driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.google.com")
    result='success'
    return jsonify({"result": result})

def close():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.quit()
    result='success'
    return jsonify({"result": result})

@app.route('/run', methods=['POST'])
def run():
    global driver
    data = request.get_json()

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    for index, obj in enumerate(data):
        for k,v in obj.items():
            print(f"  Key: {k}, Value: {v}")
        if obj["type"]=="open_app":
            driver.get(obj["id_app"])

    return jsonify({"result": data})

if __name__ == '__main__':
    app.run(port=5000)
