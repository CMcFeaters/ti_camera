<?php
//runs on NAS Client, used to access on-demand pic
//run code with IP address as "key"
$string="hey";
$val=exec("/home/pi/ti_request.py ".$_SERVER['REMOTE_ADDR'],$output,$retval);
//var_dump($output);
//var_dump($retval);
//echo "Found recent ti: ".$val;

$fileurl='/mnt/raid1/shared/TI_20220812/'.$val;
//echo($fileurl);

//header('Content-Type: image/jpeg');
//header('Content-Length: '.filesize($fileurl));
//readfile($fileurl);
header('Content-Type: image/jpeg');
header('Content-Length: '.filesize($fileurl));
readfile($fileurl);

?>
