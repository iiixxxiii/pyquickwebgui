layui.use(function () {
    var $ = layui.$;
    var form = layui.form;
    var upload = layui.upload;
    var laytpl = layui.laytpl;
    var layer = layui.layer;
    var table = layui.table;
    var element = layui.element;

    var file_path = ""
    var sheet_name = ""
    var template_editor, result_editor;
    var global_data = {}

    // $.ajax({
    //     url: '/api/test',
    //      type: "POST",
    //     contentType: "application/json",
    //     success: function (result) {
    //         layer.alert('result:' + JSON.stringify(result));
    //     }
    // });

    function load_global_data() {
        var global = layui.data('global');
        global_data = !!global.data ? global.data : {}
        console.log("load_global_data==============", global_data)
        if (JSON.stringify(global_data) != "{}") {
            template_editor.setValue(global_data.template_data);
            result_editor.setValue(global_data.result_data);
            init_sheet_data(global_data.sheet_data)
        }
    }


    function save_global_data() {
        global_data.template_data = template_editor.getValue()
        // global_data.result_data = result_editor.getValue()
        console.log("save_global_data==============", global_data)
        layui.data('global', {
            key: 'data',
            value: global_data
        });
        layer.msg('保存成功')
    }

    function show_json(json_data) {
        console.log(">>>>>>>>>show_json", json_data)
        var options = {
            collapsed: true,
            withQuotes: true
        };
        $('#json-renderer').jsonViewer({ table_data: json_data }, options);
    }

    function init_template_editor() {
        template_editor = ace.edit("template_editor", {
            mode: "ace/mode/sql",
            selectionStyle: "text"
        })
        template_editor.setTheme("ace/theme/twilight");
    }


    function init_result_editor() {
        result_editor = ace.edit("result_editor", {
            mode: "ace/mode/sql",
            selectionStyle: "text"
        })
        result_editor.setTheme("ace/theme/twilight");
    }





    function init_show_table_sheet_data(data) {
        show_json(data)
        // 渲染表格
        for (var key in data.sheet_names) {
            var sheet_name = data.sheet_names[key]
            var cols = []
            var sheet_data = data.sheet_datas[sheet_name]
            var id = "#ID-" + sheet_name
            //选择
            cols.push({
                type: 'checkbox', fixed: 'left'
            })

            for (const key in sheet_data.heads) {
                //计算 长度
                var h_width = sheet_data.heads[key].length * 30
                var v_width = !!sheet_data.data[0][sheet_data.heads[key]] ? sheet_data.data[0][sheet_data.heads[key]].length * 30 : 0
                h_width = h_width > v_width ? h_width : v_width
                h_width = h_width > 600 ? 600 : h_width
                // console.log("headseeeeeeeee", key, sheet_data.heads[key], h_width)
                cols.push({
                    title: sheet_data.heads[key],
                    field: sheet_data.heads[key],
                    width: h_width
                })
            }

            table.render({
                elem: id,
                cellMinWidth: 80,
                autoColWidth: true,
                data: sheet_data.data,
                page: true,
                cols: [cols]
            });
        }

    }


    function init_sheet_data(data) {
        console.log("...........init_sheet_data data=", data)

        // 获取模板渲染并输出结果
        laytpl($('#sheet_data').html()).render(data, function (str) {
            $(".alltable").html(str)
            init_show_table_sheet_data(data)
        })

    }


    //获取 页面 数据
    function get_sheet_data(field) {
        console.log("...........get_sheet_data field=", field)
        var index = layer.load(0, { shade: false });

        for (key in field) {
            sheet_name = field[key]
        }

        $.ajax({
            url: '/api/read_file_excel_sheet_data',
            contentType: "application/json",
            type: "POST",
            data: JSON.stringify(field),
            success: function (result) {
                console.log("...........read_file_excel_sheet_data data=", result)
                if (result.code == 0) {
                    global_data.sheet_data = result.data
                    init_sheet_data(result.data)
                } else {
                    layer.msg("错误:" + result.msg)
                }

                layer.close(index);
            }
        });
    }


    function show_select_sheet(data) {

        // 渲染并输出结果
        laytpl($('#select_sheet').html()).render(data, function (str) {
            layer.open({
                type: 1,
                content: str, // 捕获的元素
                success: function () {
                    // 对弹层中的表单进行初始化渲染
                    form.render()

                    // 表单提交事件
                    form.on('submit(select_sheet)', function (data) {
                        var field = data.field; // 获取表单字段值
                        layer.closeAll();
                        // 显示填写结果，仅作演示用
                        // layer.alert(JSON.stringify(field), {
                        // title: '当前填写的字段值'
                        // });
                        console.log("xxxxxxxxxfield", field)
                        get_sheet_data(field)
                        return false; // 阻止默认 form 跳转
                    });
                },
                end: function () {
                    // layer.msg('关闭后的回调', {icon:6});
                }
            });
        });
    }


    function init() {
        init_result_editor()
        init_template_editor()
        load_global_data()



        $(".save").click(function () {
            save_global_data()
        })



        // 多图片上传
        upload.render({
            elem: '.web_load',
            url: '',
            done: function (res) {
                // 上传完毕
                // …
            }
        });

        $(".empty").click(function () {
            global_data = {}
            $(".alltable").html("")
        })

        //渲染
        $(".rendering").click(function () {

            // 渲染并输出结果
            template_data = template_editor.getValue()
            laytpl(template_data).render({ "table_data": global_data.sheet_data }, function (str) {
                result_editor.setValue(str)
                element.tabChange('tab-hash', '33');
            })

        })

        $(".load").click(function () {
            console.log("load")
            var index = layer.load(0, { shade: false });
            $.ajax({
                url: '/api/select_file',
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({
                    initialdir: "./static/file",
                    filetypes: [["excel", ".xls .xlsx"]]
                }),
                success: function (result) {
                    console.log("==========result", result)
                    file_path = result.data.file_path
                    $.ajax({
                        url: '/api/read_file_excel',
                        type: "POST",
                        contentType: "application/json",
                        data: JSON.stringify({
                            file_path: file_path,
                        }),
                        success: function (result) {
                            if (result.code == 0) {
                                show_select_sheet(result.data)
                            } else {
                                layer.alert('result:' + JSON.stringify(result));
                            }
                            layer.close(index); // 关闭 loading
                        }
                    });
                }
            });
        })
    }
    init()



});