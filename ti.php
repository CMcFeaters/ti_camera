<?php
$val=exec("/home/pi/doodle_cam.py",$output,$retval);
//var_dump($output);
//var_dump($retval);
//echo "Found recent doodle: ".$val;

$fileurl='/mnt/raid1/shared/doodle/'.$val;
//echo($fileurl);

//header('Content-Type: image/jpeg');
//header('Content-Length: '.filesize($fileurl));
//readfile($fileurl);
header('Content-Type: image/jpeg');
header('Content-Length: '.filesize($fileurl));
readfile($fileurl);

?>
