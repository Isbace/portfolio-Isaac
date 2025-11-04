<?php session_start(); ?>
<?php
include("db_connection.php"); 
include("Header.php");
?>

<html>
<body style="background-color:#FFF8DC;">
<?php

$var = $_POST['searchbar'];
$new_var = "%".$var."%";
$sql = "SELECT * FROM books WHERE book_title LIKE '$new_var' OR author LIKE '$new_var'";
echo $sql; // Imprime la consulta SQL
$result = $connect->query($sql);
$row = $result->fetch_assoc();

if ($result->num_rows > 0) {
  while ($row = $result->fetch_assoc()) {
	echo "<a href='book_details.php?id=".$row['sid']."'>";
    echo "<img src='" . $row['cover_img'] . "' style='float: left; margin-right: 20px;' width='350' height='450'>";
    echo "<h2>" . $row['book_title'] . "</h2></a>";
    echo "<p><b>Author:</b> " . $row['author'] . "</p>";
    echo "<p><b>Genre:</b> " . $row['type_of_book'] . "</p>";
    echo "<p><b>Publisher:</b> " . $row['publisher'] . "</p>";
    echo "<p><b>Year:</b> " . $row['year_of_release'] . "</p>";
    echo "<p><b>Price:</b> $" . $row['price'] . "</p>";
    echo "<p><b>Description:</b> " . $row['information'] . "</p>";
	echo "<br>";
	echo "<br>";
	echo "<br>";
	echo "<br>";
	echo "<br>";
	echo "<br>";
	echo "<br>";
	echo "<br>";
    echo "<hr>";
  }
} else {
  echo "No results found.";
}
?>

 </body>
</html>

