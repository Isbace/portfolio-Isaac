<?php include("db_connection.php"); 
include("Header2.php") ?>

<html>
<head>
</head>
<body style="background-color:#FFF8DC;">

	  <a href="login.php"><button type="button" style="float:right;">Cancel</button></a>
	  <br><br>
<div class="form-container">
  <h2>Sign In</h2>
  <form method="POST" action="signin_process.php">
  <div class="form-group">
      <label for="name">Enter your name:</label>
      <input type="text" name="name" = "name" required>
    </div>
    <div class="form-group">
      <label for="name">Enter your username:</label>
      <input type="text" name="userid" = "userid" required>
    </div>
    <div class="form-group">
      <label for="password">Enter your password:</label>
      <input type="password" name="password" = "password" required>
    </div>
	<div class="form-group">
      <label for="role">Role:</label>
      <select name="role" required>
        <option value="U">User</option>
        <option value="A">Admin</option>
      </select>
    </div>
	<br>
	<br>
    <div class="form-group">
      <button type="submit">Sign In</button>
    </div>
  </form>
</div>

</body>
</html>
