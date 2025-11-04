<?php 
session_start();

?>

<!DOCTYPE html>
<html>


<body>

<?php 

include("db_connection.php");
$user=($_POST['userid']);
$pass=($_POST['password']);
$role=($_POST['role']);


$sql = "SELECT * FROM users_tab WHERE userid ='$user' AND password='$pass'";
$result=$connect->query($sql);
$row = $result->fetch_assoc(); 

if($row['role']==='U')  
{
	$_SESSION['userid']=$user;
	$_SESSION['password']=$pass;
	$_SESSION['role'] = "U";
	header('location: ./user/index.php');	 
}

elseif($row['role']==='A')  
{
	$_SESSION['userid']=$user;
	$_SESSION['password']=$pass;
	$_SESSION['role'] = "A";
	header('location: ./admin/index.php');	 
}

else
{
	header('location: error_page.php');
}


mysqli_close($conn);
?>


</html>