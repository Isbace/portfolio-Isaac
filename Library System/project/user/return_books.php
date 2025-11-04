<?php session_start(); ?>
<?php
include("db_connection.php");
include ("Header.php");
?>
<?php   
	$user=($_SESSION['userid']);  
	if(isset($_POST['return_book'])) {
		$book_title = $_POST['book_title'];
		$sql = "UPDATE users_tab SET my_books = REPLACE(REPLACE(my_books, '$book_title,', ''), '$book_title', '') WHERE userid = '$user'";
		$result = $connect->query($sql);
		if ($result) {
			$sql2 = "UPDATE books SET availability_status = 'Available' WHERE book_title = '$book_title'";
			$result2 = $connect->query($sql2);		
			$sql3 = "DELETE FROM lending_books WHERE book_title = '$book_title'";
			$result3 = $connect->query($sql3);			
		} 
	}
?>

<html>
<head>
</head>
<body style="background-color:#FFF8DC;">


<center> <h2> Return Books </h2> </center>
<br><br>

 <?php

$sql = "SELECT my_books FROM users_tab WHERE userid = '$user'";
$result = $connect->query($sql);

if ($result->num_rows > 0) {
  $my_books = $result->fetch_assoc()['my_books'];
  $book_titles = explode(",", $my_books);

  // Buscar los libros en la tabla "books"
  foreach ($book_titles as $book_title) {
    $book_title = trim($book_title); // eliminar espacios en blanco al inicio y al final
    $sql2 = "SELECT * FROM books WHERE book_title = '$book_title'";
    $result2 = $connect->query($sql2);

    // Imprimir la información del libro encontrado
    if ($result2->num_rows > 0) {
      $row2 = $result2->fetch_assoc();
      echo "<img src='" . $row2['cover_img'] . "' style='float: left; margin-right: 20px;' width='350' height='450'>";
      echo "<h2>" . $row2['book_title'] . "</h2>";
      echo "<p><b>Author:</b> " . $row2['author'] . "</p>";
      echo "<p><b>Genre:</b> " . $row2['type_of_book'] . "</p>";
      echo "<p><b>Publisher:</b> " . $row2['publisher'] . "</p>";
      echo "<p><b>Year:</b> " . $row2['year_of_release'] . "</p>";
      echo "<p><b>Price:</b> $" . $row2['price'] . "</p>";
      echo "<p><b>Description:</b> " . $row2['information'] . "</p>";
	  echo "<form method='post'>";
      echo "<input type='hidden' name='book_title' value='$book_title'>";
      echo "<input type='submit' name='return_book' value='Regresar libro'>";
      echo "</form>";
	  echo "<br>";
	  echo "<br>";
	  echo "<br>";
	  echo "<br>";
	  echo "<br>";
	  echo "<br>";
	  echo "<br>";
	  echo "<br>";
	  echo "<br>";
    } 	

  }
} 
echo "You do not have more books to return";

?>


</body>
</html>
