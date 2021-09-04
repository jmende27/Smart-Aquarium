def webDisplay(data1, data2, data3, data4):
    with open('index.php','w') as F:
        F.write("<html>\n<body bgcolor=\"#D6EAF8\">\n<h1>Smart Fish Tank</h1>\n<?php\n")
        F.write("$tmp="+repr(data1)+";\n$wL="+repr(data2)+";\n$amm="+repr(data3)+";\n$pH="+repr(data4)+";\n")
        F.write("?>\n<table border=\"5px\" cellpadding=\"8\" cellspacing=\"50\">\n<tr>\n<th>Temperature:</th>\n")
        F.write("<th>Water Level:</th>\n<th>Ammonia:</th>\n<th>pH:</th>\n</tr>\n<tr>\n")
        F.write("<?php\necho \"<td>$tmp</td>\";\necho \"<td>$wL</td>\";\necho \"<td>$amm</td>\";\necho \"<td>$pH</td>\";\n?>\n</tr>\n</table>\n</body>\n</html>")
    return
