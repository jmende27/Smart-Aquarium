<html>
<body bgcolor="#D6EAF8">
<h1>Smart Fish Tank</h1>
<?php
$tmp=204;
$wL=73;
$amm=99;
$pH=196;
?>
<table border="5px" cellpadding="8" cellspacing="50">
<tr>
<th>Temperature:</th>
<th>Water Level:</th>
<th>Ammonia:</th>
<th>pH:</th>
</tr>
<tr>
<?php
echo "<td>$tmp</td>";
echo "<td>$wL</td>";
echo "<td>$amm</td>";
echo "<td>$pH</td>";
?>
</tr>
</table>
</body>
</html>