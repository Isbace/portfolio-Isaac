
<?php
include("db_connection.php"); 
$user=($_SESSION['userid']);
?>

<html>
<body>

<form method="POST" action="search_books.php">
  <label for="search">Search:</label>
  <input type="text" id="search" name="searchbar" placeholder="Search books by name of the book or author..." style="width: 500px;">
  <br><br>
  <button type="submit">Search</button>
</form>


<center> <h2> Classic Novels </h2> </center>


<?php
	$sql="SELECT * FROM books WHERE type_of_book='Novela'";
	$result=$connect->query($sql);
	$count=1;
	echo "<table style='width:100%;table-layout:fixed;'>";
	echo "<tr>";
	while($row = $result->fetch_assoc())
	{
		echo "<td align='center'>";
			echo "<a href='book_details.php?id=".$row['sid']."'>";
			echo "<img src=". $row['cover_img']." width='300' height='350'>"."<br>";
			echo $row['book_title']."<br>";
			echo "$".$row['price']."<br>";
			
		echo "</td>";
		$count++;
		if($count==5)
		{
			echo "</tr><tr>";
			$count=1;
		}
	}
	echo "</table>"
?>
<center> <h2>  Kids </h2> </center>

<?php
	$sql2="SELECT * FROM books WHERE type_of_book='Kids'";
	$result2=$connect->query($sql2);
	$count=1;
	echo "<table style='width:100%;table-layout:fixed;'>";
	echo "<tr>";
	while($row2 = $result2->fetch_assoc())
	{
		echo "<td align='center'>";
			echo "<a href='book_details.php?id=".$row2['sid']."'>";
			echo "<img src=". $row2['cover_img']." width='300' height='350'>"."<br>";
			echo $row2['book_title']."<br>";
			echo "$".$row2['price']."<br>";
			
		echo "</td>";
		$count++;
		if($count==5)
		{
			echo "</tr><tr>";
			$count=1;
		}
	}
	echo "</table>"
?>

<center> <h2>  Romance </h2> </center>

<?php
	$sql3="SELECT * FROM books WHERE type_of_book='Romance'";
	$result3=$connect->query($sql3);
	$count=1;
	echo "<table style='width:100%;table-layout:fixed;'>";
	echo "<tr>";
	while($row3 = $result3->fetch_assoc())
	{
		echo "<td align='center'>";
			echo "<a href='book_details.php?id=".$row3['sid']."'>";
			echo "<img src=". $row3['cover_img']." width='300' height='350'>"."<br>";
			echo $row3['book_title']."<br>";
			echo "$".$row3['price']."<br>";
			
		echo "</td>";
		$count++;
		if($count==5)
		{
			echo "</tr><tr>";
			$count=1;
		}
	}
	echo "</table>"
?>

 </body>
</html>

