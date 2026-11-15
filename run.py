import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = os.path.join(ROOT, 'backend', 'python')
if APP_ROOT not in sys.path:
    sys.path.insert(0, APP_ROOT)

from app.main import app

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)
