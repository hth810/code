from flask import request, make_response

from App import create_app

app=create_app()

# 捕获所有OPTIONS请求并返回200状态码
@app.after_request
def after_request(response):
    if request.method == 'OPTIONS':
        response = make_response('', 200)
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response
if __name__ == '__main__':
    app.run(port=5000)
