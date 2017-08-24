<?php
if($_FILES["file"]["error"] > 0){
	echo "Error:" . $_FILES["file"]["error"];
} else{
	set_time_limit(0);
	date_default_timezone_set("Asia/Taipei");
	$start = date("d/H:i:s");
	echo "File Name : " . $_FILES["file"]["name"] . "<br/>";
	move_uploaded_file($_FILES["file"]["tmp_name"], "../data/" . $_FILES["file"]["name"]);
	exec('python ../python/main.py ' . $_FILES["file"]["name"] . ' ' . $_POST['year'], $ret);
	exec('python ../python/GetView/getView.py 1 ' . $ret[0], $filename);
	exec('python ../python/GetView/getView.py 2 ' . $ret[0], $filename2);
	exec('python ../python/GetView/getView.py 3 ' . $ret[0], $filename3);
	exec('python ../python/GetView/getView.py 4 ' . $ret[0], $filename4);
	exec('python ../python/GetView/getView.py 5 ' . $ret[0], $filename5);
	exec('python ../python/ClearData/clearData.py', $re);
	$zip = new ZipArchive();
	$ZIPfilename = "../result/Result-" . $_FILES["file"]["name"] . ".zip";
	if ($res = $zip->open($ZIPfilename)) {
		switch ($res) {
			case ZipArchive::ER_EXISTS:
				$zip->open($ZIPfilename, ZipArchive::OVERWRITE);
				break;
			default:
				$zip->open($ZIPfilename, ZipArchive::CREATE);
				break;
		}
	}

	$zip->addFile("../result/" . $ret[0] . ".txt");
	$zip->addFile("../result/" . $filename[0]);
	$zip->addFile("../result/" . $filename2[0]);
	$zip->addFile("../result/" . $filename3[0]);
	$zip->addFile("../result/" . $filename4[0]);
	$zip->addFile("../result/" . $filename5[0]);
	$zip->close();

	$end = date("d/H:i:s");
	$diff = strtotime($end) - strtotime($start); 
	$h = floor($diff / 3600);
	$diff = $diff % 3600;
	$m = floor($diff / 60);
	$s = $diff % 60;
	// echo "執行時間：" . $h . ":" . $m . ":" . $s . "<br>";
	echo "開始時間：" . $start . "<br>";
	echo "結束時間：" . $end . "<br>";
	echo "<a href='download.php?file=Result-" . $_FILES["file"]["name"] . ".zip'>Result-". $_FILES["file"]["name"] . "</a><br>";
}
?>
