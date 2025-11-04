
<!DOCTYPE html>
<html>
<body style="background-color:#FFF8DC;">

<?php 
include("db_connection.php");


$name=($_POST['name']);
$user=($_POST['userid']);
$pass=($_POST['password']);
$role=($_POST['role']);
$lid = rand(1,10000);


$sql = "INSERT INTO users_tab (sid, user_name, userid, password, role, my_books, books_returned)
		VALUES ('$lid', '$name', '$user', '$pass', '$role', '', '' )";
$result = $connect->query($sql);
if($result == FALSE)
{
	include("error_page.php");
}
else
{
	include("login.php");
}

?>


</html>