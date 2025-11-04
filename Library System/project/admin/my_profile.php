<?php 
session_start(); 
include("db_connection.php"); 
include ("Header.php"); 
$user=($_SESSION['userid']); 

$sql = "SELECT * FROM users_tab WHERE userid = '$user'"; 
$result = $connect->query($sql); 

if (!$result) {

    die("Error en la consulta: " . $connect->error);
}

$row = $result->fetch_assoc(); 
?>

<html>
<body style="background-color:#FFF8DC;">
<h2>User Information</h2>

<table border="3">
	<thead>
		<tr>
			<th>User Id</th>
			<th>User Name</th>
			<th>Role</th>
			<th>My Books</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			 <td data-th="User ID"><?php echo $row['userid']; ?></td>
			 <td data-th="User Name"><?php echo $row['user_name']; ?></td>
			 <td data-th="Role"><?php echo $row['role']; ?></td>
			 <td data-th="My Books"><?php echo $row['my_books']; ?></td>
		</tr>
	</tbody>
</table>


</body>
</html>