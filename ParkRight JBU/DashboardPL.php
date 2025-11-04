<?php
// Database connection
$servername = "localhost";
$username = "root"; // WAMP default
$password = ""; // WAMP default (empty)
$dbname = "parkrightjbu";

$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Query to get users
//$sql = "SELECT userID, name, email, building, parking_in FROM users";
//$result = $conn->query($sql);
$sql = "SELECT userID, name, email, carID, RFID_tag, building, parking_in FROM users";
$result = $conn->query($sql);


// Query to get violations
$sql_violations = "SELECT FineID, carID, timestamp, fine FROM violations";
$result_violations = $conn->query($sql_violations);

// Query to get violations history
$sql_violations_history = "SELECT FineID, carID, timestamp, fine FROM violation_history";
$result_violations_history = $conn->query($sql_violations_history);

// Query for JAlvin lot
$sql_jalvin = "SELECT COUNT(carID) AS total_cars FROM users WHERE parking_in = 'JAlvin'";
$result_jalvin = $conn->query($sql_jalvin);

// Query for Mayfield lot
$sql_mayfield = "SELECT COUNT(carID) AS total_cars FROM users WHERE parking_in = 'Mayfield'";
$result_mayfield = $conn->query($sql_mayfield);

// Query for Walker lot
$sql_walker = "SELECT COUNT(carID) AS total_cars FROM users WHERE parking_in = 'Walker'";
$result_walker = $conn->query($sql_walker);

// Query for Hutch lot
$sql_hutch = "SELECT COUNT(carID) AS total_cars FROM users WHERE parking_in = 'Hutch'";
$result_hutch = $conn->query($sql_hutch);

// Enable error reporting (for debugging)
error_reporting(E_ALL);
ini_set('display_errors', 1);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Parking Lot Dashboard</title>
    <link rel="stylesheet" href="StylesPL.css">
    <link rel="stylesheet" href="StylesPL.css?v=<?php echo time(); ?>">
</head>
<body>
    <div class="container">
        <!-- Left Sidebar (Menu) -->
        <aside class="menu">
            <h2>ParkRight JBU</h2>
            <button onclick="showSection('students')">Students</button>
            <button onclick="showSection('violations')">Violations</button>
            <button onclick="showSection('violations-history')">Violations History</button>
            <button onclick="showAllSections()">View All</button>
        </aside>
        
        <!-- Main Section (Middle) -->
        <main class="main-content">
        <h2 id="students">Students Information</h2>
            <div id="students-section" class="Students-container">
                <table class="Students">
                    <thead>
                        <tr>
                            <th>User ID</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Car ID</th>
                            <th>RFID Tag</th>
                            <th>Building</th>
                            <th>Parking In</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php while ($row = $result->fetch_assoc()): ?>
                            <tr>
                                <td><?php echo $row['userID']; ?></td>
                                <td><?php echo $row['name']; ?></td>
                                <td><?php echo $row['email']; ?></td>
                                <td><?php echo $row['carID']; ?></td>
                                <td><?php echo $row['RFID_tag']; ?></td>
                                <td><?php echo $row['building']; ?></td>
                                <td><?php echo $row['parking_in']; ?></td>
                            </tr>
                        <?php endwhile; ?>
                    </tbody>
                </table>
            </div>
            <h2>Violations</h2>
            <div id="violations-section" class="Violations-container">
                <table class="Violations">
                    <thead>
                        <tr>
                            <th>Fine ID</th>
                            <th>Car ID</th>
                            <th>Timestamp</th>
                            <th>Fine</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php while ($row = $result_violations->fetch_assoc()): ?>
                            <tr>
                                <td><?php echo $row['FineID']; ?></td>
                                <td><?php echo $row['carID']; ?></td>
                                <td><?php echo $row['timestamp']; ?></td>
                                <td><?php echo $row['fine']; ?></td>
                            </tr>
                        <?php endwhile; ?>
                    </tbody>
                </table>
            </div>
            <h2>Violations History</h2>
            <div id="violations-history-section" class="ViolationsHistory-container">
                <table class="ViolationsHistory">
                    <thead>
                        <tr>
                            <th>Fine ID</th>
                            <th>Car ID</th>
                            <th>Timestamp</th>
                            <th>Fine</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php while ($row = $result_violations_history->fetch_assoc()): ?>
                            <tr>
                                <td><?php echo $row['FineID']; ?></td>
                                <td><?php echo $row['carID']; ?></td>
                                <td><?php echo $row['timestamp']; ?></td>
                                <td><?php echo $row['fine']; ?></td>
                            </tr>
                        <?php endwhile; ?>
                    </tbody>
                </table>
            </div>
        </main>
    </div>

    <script>
        // JavaScript function to show/hide sections based on button clicked
        function showSection(section) {
            // Hide all sections
            document.getElementById('students-section').style.display = 'none';
            document.getElementById('violations-section').style.display = 'none';
            document.getElementById('violations-history-section').style.display = 'none';

            // Show the selected section
            if (section === 'students') {
                document.getElementById('students-section').style.display = 'block';
            } else if (section === 'violations') {
                document.getElementById('violations-section').style.display = 'block';
            } else if (section === 'violations-history') {
                document.getElementById('violations-history-section').style.display = 'block';
            }
        }

        function showAllSections() {
            document.getElementById('students-section').style.display = 'block';
            document.getElementById('violations-section').style.display = 'block';
            document.getElementById('violations-history-section').style.display = 'block';
        }

        // Initially display all sections
        document.getElementById('students-section').style.display = 'block';
        document.getElementById('violations-section').style.display = 'block';
        document.getElementById('violations-history-section').style.display = 'block';
    </script>


</body>
</html>