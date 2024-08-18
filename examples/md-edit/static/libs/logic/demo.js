layui.use(function () {
    var $ = layui.$;
    var form = layui.form;
    var upload = layui.upload;
    var layer = layui.layer;

    $(".test").click(function(){
         console.log(".test")
         $.post('/api/test', function (result, status) {
                console.log("数据: ", result, "状态: ", status);
                layer.alert('result:'+ JSON.stringify(result));
        });
    })


    console.log("layui.use")

});