<?php
if($_FILES["sfx"]["error"] > 0){
	echo "Error:" . $_FILES["sfx"]["error"];
} else{
	set_time_limit(0);
	$start = date("H:i:s");
	echo "File Name(sfx) : " . $_FILES["sfx"]["name"] . "<br/>";
	echo "File Name(theme) : " . $_FILES["theme"]["name"] . "<br/>";
	move_uploaded_file($_FILES["sfx"]["tmp_name"], "../data/" . $_FILES["sfx"]["name"]);
	move_uploaded_file($_FILES["theme"]["tmp_name"], "../data/" . $_FILES["theme"]["name"]);
	exec('python ../python/WriteDB/main.py ' . $_FILES["sfx"]["name"] . ' ' . $_FILES["theme"]["name"] . ' ' . $_POST['year'], $ret);
	echo ('上傳完成<br>');
	$end = date("H:i:s");
	$diff = strtotime($end) - strtotime($start); 
	$h = floor($diff / 3600);
	$diff = $diff % 3600;
	$m = floor($diff / 60);
	$s = $diff % 60;
	echo "執行時間：" . $h . ":" . $m . ":" . $s . "<br>";
}
?>