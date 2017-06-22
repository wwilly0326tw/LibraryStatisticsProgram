<?php
	set_time_limit(0);
	exec('python ../python/WriteDB/deleteData.py ' . $_POST['year'], $ret);
	echo('刪除完成');
?>