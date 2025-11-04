<?php
session_start();
if(($_SESSION['role'] !="U"))
{
echo "You are trying to access a BAD Page. <a href='login.php' >Login Again</a> ";
session_destroy();

}
else{
?>
<html>
<head>
	<title>University System</title>
</head>
<body style="background-color:#FFF8DC;">
<?php 
	$user=($_SESSION['userid']);
	include ("Header.php"); 
	include("db_connection.php");	
	include ("user_page.php");

	?>

<div id="wrapper">
<table align=center bgcolor="#FFFFFF" width=1000px>
<tr><td>

<?php
if(isset($_SESSION['userid']))
{
?>

<?php 
		include ("db_connection.php");
		$user=($_SESSION['userid']);
?>
      
<?php

}
else
{
   echo "session expired";

}
?> 
<?php }?>  
</form>

</td></tr></table>

</div>


      </body>
</html>