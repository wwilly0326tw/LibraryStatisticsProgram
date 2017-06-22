<?php
	echo ('查詢年分：' . $_POST['year']);
	echo ('<br>');
	exec('python ../python/GetView/getView.py 6 0 ' . $_POST['year'] , $filename);
	echo "<a href='download.php?file=" . $filename[0] . "'>不支援主題表</a><br>";
?>