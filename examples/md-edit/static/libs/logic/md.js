layui.use(function () {
    var $ = layui.$;
    var form = layui.form;
    var upload = layui.upload;
    var layer = layui.layer;
    var file_path = ""

    var contentEditor = new Vditor('vditor', {
        height: "100%",
        toolbarConfig: {
            pin: true,
        },
        cache: {
            enable: false,
        },
        "mode": "sv",
        "preview": {
            "mode": "both"
        },
        after: () => {
            contentEditor.setValue('hello, Vditor + Vue!')
        },
        // customRenders: [{  render: (elemen, vditor) => {
        //     window.VditorI18n["load"] = "加载文件"
        //     console.log("customRenders")
        // }} ],
        toolbar: [
            {
                name: "file",
                icon: '文件',
                tipPosition: "ne",
                className: 'btext',
                toolbar: [
                    {
                        name: "load",
                        hotkey: '⇧n',
                        // tipPosition: "ne",
                        icon: '加载文件 Ctrl+n',
                        // className: "right",
                        click(event, vditor) {
                            var index = layer.load(0, {shade: false});
                            $.post({
                                url: '/api/select_file',
                                contentType: "application/json",
                                data: JSON.stringify({
                                    initialdir: "./static/file",
                                    filetypes: [["Markdown", ".md"], ['All Files', ' *']]
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
                                                contentEditor.setValue(result.data)
                                                layer.msg('读取成功');
                                          }else{
                                                layer.alert('result:' + JSON.stringify(result));
                                          }
                                          layer.close(index); // 关闭 loading

                                        }
                                    });
                                }
                            });
                        },
                    },
                    {
                        name: "save",
                        name: "load",
                        hotkey: '⇧s',
                        // tipPosition: "ne",
                        icon: '保存文件 Ctrl+s',
                        click(event, vditor) {
                            console.log(".savefile",event, vditor)
                            $.post({
                                url: '/api/save_file',
                                contentType: "application/json",
                                data: JSON.stringify({
                                    textval:  contentEditor.getValue(),
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
                        },
                    },
                ],
            },
            "emoji",
            "headings",
            "bold",
            "italic",
            "strike",
            "link",
            "|",
            "list",
            "ordered-list",
            "check",
            "outdent",
            "indent",
            "|",
            "quote",
            "line",
            "code",
            "inline-code",
            "insert-before",
            "insert-after",
            "|",
            "upload",
            "record",
            "table",
            "|",
            "undo",
            "redo",
            "|",
            "fullscreen",
            "edit-mode",
            {
                name: "more",
                toolbar: [
                    "both",
                    "code-theme",
                    "content-theme",
                    "export",
                    "outline",
                    "preview",
                    "devtools",
                    "info",
                    "help",
                ],
            },
        ],
    })
});