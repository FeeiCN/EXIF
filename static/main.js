$(document).ready(function () {
    var map = new AMap.Map("container", {
        resizeEnable: true,
        zoom: 5
    });
    // http://hayageek.com/docs/jquery-upload-file.php#doc
    $("#fileuploader").uploadFile({
        url: "/upload",
        fileName: "file",
        showPreview: true,
        uploadStr: '选择上传图片(<20M)',
        dragDropStr: '拖拽图片到此处',
        onSuccess: function (files, data, xhr, pd) {
            $('ul.image-data').html('');
            $('ul.gps-data').html('');
            $('ul.exif-data').html('');
            $('.profpic')[0].src = $('.ajax-file-upload-preview')[0].src;
            console.log(files);
            console.log(data);
            jQuery.each(data, function (key, val) {
                var ul = $('ul.' + key + '-data');
                ul.html('');
                for (var i = 0; i < val.length; i++) {
                    ul.append("<li>" + val[i] + '</li>');
                }
            });
            console.log(xhr);
            console.log(pd);
            // window.history.pushState('page2', 'Title', data['other']['filename']);
            //files: list of files
            //data: response from server
            //xhr : jquer xhr object
            var lnglatXY = [data['other']['GPSLongitude'], data['other']['GPSLatitude']]; //已知点坐标
            function regeocoder() {  //逆地理编码
                var geocoder = new AMap.Geocoder({
                    radius: 1000,
                    extensions: "all"
                });
                geocoder.getAddress(lnglatXY, function (status, result) {
                    console.log(result);
                    if (status === 'complete' && result.info === 'OK') {
                        geocoder_CallBack(result);
                    }
                });
                var marker = new AMap.Marker({  //加点
                    map: map,
                    position: lnglatXY
                });
                map.setFitView();
            }

            function geocoder_CallBack(data) {
                var address = data.regeocode.formattedAddress; //返回地址描述
                $('.tag').text(address);
            }

            regeocoder()
        }
    });
});