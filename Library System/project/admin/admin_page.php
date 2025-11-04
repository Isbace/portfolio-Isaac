<?php
include("db_connection.php"); 
$user=($_SESSION['userid']);
?>

<html>
<body>

<div>
  <h1>Right Aligned</h1>
  <a href="#"><button> Submit </button></a>
  <br />
</div>
<hr />
<div class="left">
  <h1>Left Aligned</h1>
  <a href="#" class="btn">Submit <span class="arrow">❯</span></a>
  <br />
</div>
<hr />
<div class="center">
  <h1>Center Aligned</h1>
  <a href="#" class="btn">Submit <span class="arrow">❯</span></a>
  <br />
</div>


</html>
</body>
