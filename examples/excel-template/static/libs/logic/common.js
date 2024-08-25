var tool = {}

tool.day = function(){
    return dayjs().format('YYYY-MM-DD HH:mm:ss')
}


tool.time_stamp = function(){
    return parseInt(new Date().getTime()/1000)
}
tool.time_str  = function(){
    return dayjs().format('YYYY-MM-DD HH:mm:ss')
}

 






tool.txt2sql = function(txt){
    console.log(".............txt2sql")
    var re = /'(.)'*/g;
    var newstr = txt.replace(re, (str) => {
        console.log('正则匹配到的内容', str.trim());
        return `'${str.trim()}'`;
    });
    return newstr
}


tool.split = function(txt , separator , index){
    return txt.split (separator)[index]
}


tool.split_excelval = function(txt){
    return tool.split (txt , "|" ,  1)
}

tool.url_encode = function(data){
    new_data = {}
    for(key in data){
    	 new_data[key] = encodeURIComponent(data[key])
    }
    return new_data
}

tool.download  = function (fileName, text) {
    const url = window.URL || window.webkitURL || window;
    const blob = new Blob([text]);
    const saveLink = document.createElementNS('http://www.w3.org/1999/xhtml', 'a');
    saveLink.href = url.createObjectURL(blob);
    // 设置 download 属性
    saveLink.download = fileName;
    saveLink.click();
}

tool.strlength  = function ( str ) {
    var l = 0
    console.log('str', str );
    if(str){
        str = new String(str.trim())
        l = str.length
    }

    return l
}




tool.read_file  = function(model) {
    return new Promise((resolve) => {
        // 谷歌
        if (window.FileReader) {
            // 获取文件流
            let file = model.currentTarget ? model.currentTarget.files[0] : model;
            // 创建FileReader实例
            let reader = new FileReader();
            // 读文件
            reader.readAsText(file);
            //reader.readAsText(fileObj.files[0].file, 'UTF-8');
            reader.onload = () => {
                resolve(reader.result)
            }
        }
        //支持IE 7 8 9 10
        else if (typeof window.ActiveXObject != 'undefined') {
            let xmlDoc;
            xmlDoc = new ActiveXObject("Microsoft.XMLDOM");
            xmlDoc.async = false;
            resolve(xmlDoc.load(model))
        }
        //支持FF
        else if (document.implementation && document.implementation.createDocument) {
            let xmlDoc;
            xmlDoc = document.implementation.createDocument("", "", null);
            xmlDoc.async = false;
            resolve(xmlDoc.load(model))
        }
    })
}