from src.factory import create_app
from src.config import Config

# 수정 확인
app = create_app(config=Config(), mode='DEVELOPMENT')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)