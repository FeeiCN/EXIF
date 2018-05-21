# EXIF

## 部署
```bash
pip install -r requirements.txt
# Test
python -m flask run --host 0.0.0.0
# Deploy
gunicorn app:app -w 4 -b 0.0.0.0:5000 > /tmp/exif.log 2>&1 &

# Stop
ps aux | grep gunicorn | awk '{print $2}' | xargs kill -9
```