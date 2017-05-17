<?php
if($_FILES["file"]["error"] > 0){
	echo "Error:" . $_FILES["file"]["error"];
} else{
	set_time_limit(900);
	echo "File Name : " . $_FILES["file"]["name"] . "<br/>";
	move_uploaded_file($_FILES["file"]["tmp_name"], "../data/" . $_FILES["file"]["name"]);
	exec('python ../python/main.py ' . $_FILES["file"]["name"], $ret);	
	exec('python ../python/GetView/getView.py 2 ' . $ret[0], $filename);
	exec('python ../python/GetView/getView.py 3 ' . $ret[0], $filename2);
	exec('python ../python/GetView/getView.py 4 ' . $ret[0], $filename3);

	$zip = new ZipArchive();
	$ZIPfilename = "../result/Result(" . $ret[0] . ").zip";
	if ($zip->open($ZIPfilename, ZipArchive::CREATE)!==TRUE) {
    	exit("cannot open <$filename>\n");
	}
	$zip->addFile("../result/" . $ret[0] . ".txt");
	$zip->addFile("../result/" . $filename[0]);
	$zip->addFile("../result/" . $filename2[0]);
	$zip->addFile("../result/" . $filename3[0]);
	$zip->close();
	echo "<a href='download.php?file=Result(".$ret[0].").zip'>Result(". $ret[0] . ")</a><br>";
}
?>
