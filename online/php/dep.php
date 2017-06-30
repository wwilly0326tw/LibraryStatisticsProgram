<?php
if($_FILES["dep"]["error"] > 0){
	echo "Error:" . $_FILES["dep"]["error"];
} else{
	set_time_limit(0);
	$start = date("H:i:s");
	echo "File Name(dep) : " . $_FILES["dep"]["name"] . "<br/>";
	move_uploaded_file($_FILES["dep"]["tmp_name"], "../data/" . $_FILES["dep"]["name"]);
	exec('python ../python/WriteDB/writeDepartment.py ' . $_FILES["dep"]["name"], $ret);
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