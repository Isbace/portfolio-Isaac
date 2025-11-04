
<?php 
include("Header2.php") 
?>
<!DOCTYPE html>
<html>
  <head>
    <title> Log In </title>
	<style>

    </style>
	<link rel="stylesheet" href="style.css">

  </head>
  <body style="background-color: #FDEBD0;">

	<br><br>
<div class="form-container">
  <h2>Log In</h2>
  <form method="POST" action="login_process.php">
    <div class="form-group">
      <label for="name">User:</label>
      <input type="text" name="userid" = "userid" required>
    </div>
    <div class="form-group">
      <label for="password">Password:</label>
      <input type="password" name="password" = "password" required>
    </div>
	<div class="form-group">
		<label for="role">Role:</label>
		<input type="text" name="role" = "role" required>
	</div>
	<br>
	<br>
    <div class="form-group">
      <button type="submit">Log In</button>
    </div>
  </form>
</div>
<a href="signup.php" class="button">Click here to create a new account</a>
		
 </body>
</html>
