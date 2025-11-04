	<?php session_start(); ?>
	<?php
	include("db_connection.php");
	include ("Header.php");
	?>

	<?php
	  $id = $_GET['id'];
	  $user=($_SESSION['userid']);  
	?>

	<html>
	<head>
	</head>
	<body style="background-color:#FFF8DC;">

	<?php
		
		$book_id = $_GET['id'];
		$sql = "SELECT * FROM books WHERE id = $book_id";
		$result = $connect->query($sql);
		$row = $result->fetch_assoc();

		echo "<img src='" . $row['cover_img'] . "' style='float: left; margin-right: 20px;' width='350' height='450'>";
		echo "<h2>" . $row['book_title'] . "</h2>";
		echo "<p><b>Author:</b> " . $row['author'] . "</p>";
		echo "<p><b>Genre:</b> " . $row['type_of_book'] . "</p>";
		echo "<p><b>Publisher:</b> " . $row['publisher'] . "</p>";
		echo "<p><b>Year:</b> " . $row['year_of_release'] . "</p>";
		echo "<p><b>Price:</b> $" . $row['price'] . "</p>";
		echo "<p><b>Description:</b> " . $row['information'] . "</p>";
		
		
		echo "<form id='add-to-cart-form' method='POST'>";
		echo "<input type='hidden' name='id' value='" . $id . "'>";
		echo "<input type='hidden' name='book_title' value='" . $row['book_title'] . "'>";
		echo "<input type='hidden' name='price' value='" . $row['price'] . "'>";
		echo "<label for='date_of_lending'>Date of lending:</label>";
		echo "<input type='date' id='date_of_lending' name='date_of_lending' required>";
		echo "<label for='date_of_return'>Date of return:</label>";
		echo "<input type='date' id='date_of_return' name='date_of_return' required>";
		echo "<label for='remarks' >Remarks:</label>";
		echo "<input type='text' id='remarks' name='remarks'";
		echo "<label for='status'>Status:</label>";
		echo "<input type='text' id='status' name='status'";
		echo "<br>";

		echo "<button type='submit'>Agregar al carrito</button>";
		echo "</form>";

		if ($_SERVER['REQUEST_METHOD'] === 'POST') {

			$book_id = $_POST['id'];
			$book_title = $_POST['book_title'];
			$date_of_lending = $_POST['date_of_lending'];
			$date_of_return = $_POST['date_of_return'];
			$remarks = $_POST['remarks'];
			$status = $_POST['status'];

			$sql = "SELECT availability_status FROM books WHERE id = '$book_id'";
			$result = $connect->query($sql);
			$row = $result->fetch_assoc();

			if ($row['availability_status'] == 'Available') {
				$sql = "UPDATE books SET availability_status = 'Not Available' WHERE id = '$book_id'";
				$result = $connect->query($sql);
				
				$sql = "UPDATE users_tab SET my_books = CONCAT(my_books, '$book_title ,') WHERE userid = '$user'";
				$result = $connect->query($sql);


				$sql = "INSERT INTO lending_books (id, book_title, name, date_of_lending, date_of_return, status, remarks) VALUES ('$book_id', '$book_title', '$user', '$date_of_lending', '$date_of_return', '$status', '$remarks')";
				$result = $connect->query($sql);

				if ($result) {
					echo "<p>El libro ha sido añadido al carrito.</p>";
				} else {
					echo "<p>Ha habido un error al añadir el libro al carrito.</p>";
				}
			} else {
				echo "<p>Lo siento, este libro ya ha sido prestado.</p>";
			}

		}
	?>



	</body>
	</html>
