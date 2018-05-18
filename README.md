# EXIF

## 部署
```bash
pip install -r requirements.txt
# Test
python -m flask run --host 0.0.0.0
# Deploy
gunicorn app:app -w 4 -b 0.0.0.0:5000
```