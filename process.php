<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $mac = escapeshellarg($_POST["mac"]);
    $dhcp_type = escapeshellarg($_POST["dhcp_type"]);

    // Execute Python script
    $command = "python3 network_config.py $mac $dhcp_type";
    $output = shell_exec($command);
    $result = json_decode($output, true);

    if (isset($result["error"])) {
        echo "<h3>Error: " . htmlspecialchars($result["error"]) . "</h3>";
    } else {
        echo "<h3>Assigned IP Details:</h3>";
        echo "<p>MAC Address: " . htmlspecialchars($result["mac_address"]) . "</p>";
        echo "<p>Assigned IP: " . htmlspecialchars($result["assigned_ip"]) . "</p>";
        echo "<p>Lease Time: " . htmlspecialchars($result["lease_time"]) . "</p>";
    }
} else {
    echo "<h3>Invalid request.</h3>";
}
?>
