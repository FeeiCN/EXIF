# EXIF - EXIF Information Viewer(读取照片中隐藏的各类信息)

![EXIF](http://feei.cn/images/exif_03.jpg)

## Features
- 图片信息：文件大小、长宽高、文件类型
- GPS信息：地图位置、地理位置、经纬度、速度、海拔、日期
- EXIF信息：闪光灯、光圈、亮度、快门速度、场景、白平衡、曝光模式、镜头信息
- 拍摄设备信息：设备制造公司、设备型号、软件版本、拍摄时间
- 图片被修图软件编辑过信息：PhotoShop、美图

## Usage

```bash
# Clone
git clone https://github.com/FeeiCN/EXIF && cd EXIF

pip install -r requirements.txt

# Test
python -m flask run --host 0.0.0.0

# Deploy
gunicorn app:app -w 4 -b 0.0.0.0:5000 > /tmp/exif.log 2>&1 &

# Stop
ps aux | grep gunicorn | awk '{print $2}' | xargs kill -9
```

## Reference

- [EXIF - 隐藏在图片中的重要信息](http://feei.cn/exif)