   
function createDocument()
{
	if(typeof arguments.callee.activeXString!="string")
		{
			var versions=["MSXML2.DOMDocument.6.0", "MSXML2.DOMDocument.3.0", "MSXML2.DOMDocument"],
				i,len;
			for(i=0,len=versions.length;i<len;i++)
				{
					try{
						new ActiveXobject(versions[i]);
						arguments.callee.activeXString=versions[i];
						break;
						}catch(ex)
						{}
				}
		}
}
loadXML = function (xmlFile) {
    	var xmlDoc = null;
    	//判断浏览器的类型
    	//支持IE浏览器
    	if (!window.DOMParser && window.ActiveXObject) {
    		var xmlDomVersions = ["MSXML2.DOMDocument.6.0", "MSXML2.DOMDocument.3.0", "MSXML2.DOMDocument"];
    		for (var i = 0; i < xmlDomVersions.length; i++) {
    			try {
    				xmlDoc = new ActiveXObject(xmlDomVersions[i]);
    				break;
    			}
    			catch (e) {}
    		}
    	}
    	//支持Mozilla浏览器
    	else if (document.implementation && document.implementation.createDocument) {
    		try {
    			/* document.implementation.createDocument('','',null); 方法的三个参数说明
    			 * 第一个参数是包含文档所使用的命名空间URI的字符串； 
    			 * 第二个参数是包含文档根元素名称的字符串； 
    			 * 第三个参数是要创建的文档类型（也称为doctype）
    			 */
    			xmlDoc = document.implementation.createDocument('', '', null);
    		}
    		catch (e) {}
    	}
    	else {
    		return null;
    	}
    	if (xmlDoc != null) {
    		xmlDoc.async = false;
    		xmlDoc.loadXML(xmlFile);
    	}
    	return xmlDoc;
    };
loadXMlJquery=function()
{
	$.ajax({      
				url: 'xml/mw.xml'
				,       type: 'GET'
				,       dataType: 'xml'
				,       timeout: 1000
				,       cache: false
				,       error: function (xml) {        
					alert('加载XML文档出错');      
				}
				,       success: function (xml) {         //建立一个代码片段
					//console.log($(xml));
					return $(xml);
					        
					/**var frag = $("<ul/>");         //遍历所有student节点
					        
					$(xml).find("mw").each(function (i) {           //获取id节点
						         alert($(this).children("filename").text());
						alert($(this).children("address").text());
						

					});**/         //最后得到的frag添加进HTML文档中
					        
					//frag.appendTo("#load");      
				}    
			});
}