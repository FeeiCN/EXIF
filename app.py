#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    EXIF
    ~~~~
    Implements EXIF main
    Usage:
        python app.py
    :author:    Feei <feei@feei.cn>
    :homepage:  https://github.com/FeeiCN/EXIF
    :license:   GPL, see LICENSE for more details.
    :copyright: Copyright (c) 2018 Feei. All rights reserved
"""
import os
import hashlib
import datetime
import platform
import exifread
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp/exif'
ALLOWED_EXTENSIONS = ('pdf', 'jpg', 'jpeg', 'png', 'gif', 'bmp')
"""
''  : 为空则未想好翻译内容
None: 为None则不予显示
"""
TRANSLATE_KEY = {
    'Image Make': '机器制造',  # Apple
    'Image Model': '机器模型',  # iPhone X
    'Image XResolution': '图片分辨率(X)',  # 72
    'Image YResolution': '图片分辨率(Y)',  # 72
    'Image ResolutionUnit': '分辨率单位',  # Pixels/Inch
    'Image Software': '软件版本',  # 11.3
    'Image DateTime': '拍摄时间',  # 2018:05:04 18:45:32
    'Image TileWidth': '图片平铺宽度',  # 512
    'Image TileLength': '图片平铺长度',  # 512
    'Image ExifOffset': None,  # 204
    'Image Orientation': '图片方向',  # Horizontal (normal)
    'GPS GPSLatitudeRef': None,  # N
    'GPS GPSLatitude': 'GPS纬度(N)',  # [39, 16, 2259/50]
    'GPS GPSLongitudeRef': None,  # E
    'GPS GPSLongitude': 'GPS经度(E)',  # [99, 48, 897/25]
    'GPS GPSAltitudeRef': None,  # 0
    'GPS GPSAltitude': 'GPS高度',  # 44355/32
    'GPS GPSTimeStamp': 'GPS时间',  # [10, 45, 31]
    'GPS GPSSpeedRef': None,  # K
    'GPS GPSSpeed': 'GPS速度',  # 0(公里每小时)
    'GPS GPSImgDirectionRef': None,  # T
    'GPS GPSImgDirection': 'GPS方向',  # 7067/1037
    'GPS GPSDestBearingRef': None,  # T
    'GPS GPSDestBearing': 'GPS方位',  # 7067/1037
    'GPS GPSDate': 'GPS日期',  # 2018:05:04
    'GPS Tag 0x001F': 'GPS Tag',  # 10
    'Image GPSInfo': 'GPS信息',  # 1754
    'EXIF ExposureTime': '曝光时间',  # 1/15
    'EXIF FNumber': 'F数',  # 9/5
    'EXIF ExposureProgram': '曝光程序',  # Program Normal
    'EXIF ISOSpeedRatings': 'ISO感光等级',  # 40
    'EXIF ExifVersion': 'EXIF版本',  # 0221
    'EXIF DateTimeOriginal': '原始时间',  # 2018:05:04 18:45:32
    'EXIF DateTimeDigitized': '数字时间',  # 2018:05:04 18:45:32
    'EXIF ComponentsConfiguration': '组件peizhi ',  # YCbCr
    'EXIF ShutterSpeedValue': '快门速度',  # 3303/845
    'EXIF ApertureValue': '光圈',  # 2159/1273
    'EXIF BrightnessValue': '亮度',  # 3694/1557
    'EXIF ExposureBiasValue': '曝光补偿',  # 0
    'EXIF MeteringMode': '测光模式',  # Pattern
    'EXIF Flash': '闪光灯',  # Flash did not fire, auto mode
    'EXIF FocalLength': '焦距',  # 4
    'EXIF SubjectArea': '主体区域',  # [2015, 1511, 2217, 1330]
    'EXIF SubSecTimeOriginal': '子原始时间',  # 357
    'EXIF SubSecTimeDigitized': '子数字时间',  # 357
    'EXIF FlashPixVersion': 'FlashPix版本',  # 0100
    'EXIF ExifImageWidth': '图片宽度',  # 3662
    'EXIF ExifImageLength': '图片高度',  # 2744
    'EXIF SensingMethod': '传感方式',  # One-chip color area
    'EXIF SceneType': '场景类型',  # Directly Photographed
    'EXIF ExposureMode': '曝光模式',  # Auto Exposure
    'EXIF WhiteBalance': '白平衡',  # Auto
    'EXIF FocalLengthIn35mmFilm': '35mm胶片',  # 28
    'EXIF SceneCaptureType': '场景模式',  # Standard
    'EXIF LensSpecification': '镜头规格',  # [4, 6, 9/5, 12/5]
    'EXIF LensMake': '镜头制造',  # Apple
    'EXIF LensModel': '镜头模型',  # iPhone X back dual camera 4mm f/1.8
}

TRANSLATE_VALUE = {
    'Auto': '自动',
    'Standard': '标准',
    'Auto Exposure': '自动曝光',
    'Directly Photographed': '直接拍摄',
    'Program Normal': '程序正常',
    'Flash did not fire, auto mode': '闪光灯未触发（自动模式）'
}

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024


def creation_date(path):
    if platform.system() == 'Windows':
        t = os.path.getctime(path)
    else:
        stat = os.stat(path)
        try:
            t = stat.st_birthtime
        except AttributeError:
            t = stat.st_mtime
    return datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')


def modification_date(path):
    return datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S')


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def file_size(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)


def cover_gps(n1, n2, n3):
    # [39, 16, 2259/50]
    # [99, 48, 897/25]
    # 39 + 16/60 + (2259/50)/3600 = 39.279216667
    # 99 + 48/60 + (897/25)/3600 = 99.809966667
    return float(n1) + (float(n2) / 60) + (float(n3) / 3600)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def read_exif(path):
    data = {
        'image': [],
        'other': {}
    }

    # 基础信息
    data['image'].append('文件类型: {type}'.format(type=os.path.splitext(path)[1].upper()))
    data['image'].append('文件创建时间: {time}'.format(time=creation_date(path)))
    data['image'].append('文件修改时间: {time}'.format(time=modification_date(path)))
    data['image'].append('文件大小: {size}'.format(size=file_size(path)))

    f = open(path, 'rb')
    tags = exifread.process_file(f)
    for key, value in tags.items():
        key = key.strip()
        if key not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            t_tag = key
            if key in TRANSLATE_KEY and TRANSLATE_KEY[key] != '':
                t_tag = TRANSLATE_KEY[key]
                if t_tag is None:
                    print('SKIP TAG', key)
                    continue
            t_value = value
            if str(value) in TRANSLATE_VALUE and TRANSLATE_VALUE[str(value)] != '':
                t_value = TRANSLATE_VALUE[str(value)]
            print(t_tag, '-', t_value)

            # Special Cover Value
            if key in ['GPS GPSLatitude', 'GPS GPSLongitude']:
                tmp_v = str(t_value).replace('[', '').replace(']', '').split(', ')
                t_value = cover_gps(tmp_v[0], tmp_v[1], float(int(tmp_v[2].split('/')[0]) / int(tmp_v[2].split('/')[1])))
                data['other'][key.split(' ')[1]] = t_value
            if key in ['EXIF DateTimeOriginal', 'EXIF DateTimeDigitized', 'Image DateTime', 'GPS GPSDate']:
                if ' ' in str(t_value):
                    t_value = '{date} {time}'.format(date=str(t_value).split(' ')[0].replace(':', '-'), time=str(t_value).split(' ')[1])
                else:
                    t_value = str(t_value).replace(':', '-')

            if 'Image ' in key:
                tag = 'image'
            elif 'GPS ' in key:
                tag = 'gps'
            elif 'EXIF ' in key:
                tag = 'exif'
            else:
                tag = key
            v = '{t_tag}: {v}'.format(t_tag=t_tag, v=str(t_value))
            if tag in data:
                print(v)
                data[tag].append(v)
            else:
                data[tag] = [v]
        else:
            print('NOT IN', key, value)
    return data


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'status': 404, 'message': 'no file field'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 404, 'message': 'no selected file'})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        md5 = hashlib.md5(filename.encode('utf-8')).hexdigest()
        filename = '{md5}{ext}'.format(md5=md5, ext=os.path.splitext(filename)[1])
        path_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path_file)
        data = read_exif(path_file)
        data['other']['filename'] = filename
        return jsonify(data)


if __name__ == '__main__':
    app.run()
