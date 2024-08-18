layui.use(function () {
    var $ = layui.$;
    var form = layui.form;
    var upload = layui.upload;
    var layer = layui.layer;

    $(".test").click(function () {
        console.log(".test")
        $.post('/api/test', function (result, status) {
            console.log("数据: ", result, "状态: ", status);
            layer.alert('result:' + JSON.stringify(result));
        });
    })

var file_path = ""

    $(".openfile").click(function () {
        console.log(".openfile")
        var index = layer.load(0, {shade: false});
        $.post({
            url: '/api/select_file',
            contentType: "application/json",
            data: JSON.stringify({
                initialdir: "./static/file",
                filetypes: [["txt", ".txt"], ['All Files', ' *']]
            }),
            success: function (result) {
                file_path = result.data.file_path
                $.post({
                    url: '/api/read_file',
                    contentType: "application/json",
                    data: JSON.stringify({
                        file_path:file_path ,
                    }),
                    success: function (result) {
                        console.log("数据: ", result );
                     if(result.code==0){
                            $(".textval").val(result.data)
                            layer.msg('读取成功');
                      }else{
                            layer.alert('result:' + JSON.stringify(result));
                      }
                      layer.close(index); // 关闭 loading

                    }
                });
            }
        });
    })

    $(".savefile").click(function () {
        console.log(".savefile")
        $.post({
            url: '/api/save_file',
            contentType: "application/json",
            data: JSON.stringify({
                textval:  $(".textval").val(),
                file_path: file_path
            }),
            success: function (result) {
                console.log("数据: ", result );
                if(result.code==0){
                    layer.alert('保存成功');
                }else{
                    layer.alert('result:' + JSON.stringify(result));
                }
            }
        });
    })

    console.log("layui.use")

});