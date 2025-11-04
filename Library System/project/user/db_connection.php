<?php
	$connect = new mysqli("localhost", "root", "", "project");
		if($connect-> connect_errno){
			die('Could not connect: ' . $connect->connect_errno);
			}		
?>