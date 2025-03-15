<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Convertion DHCPV4 or DHCPV6 </title>
</head>
<body>
    <h2>Request an IP Address</h2>
    <form action="process.php" method="POST">
        <label for="mac">MAC Address:</label>
        <input type="text" id="mac" name="mac" required placeholder="00:1A:2B:3C:4D:5E">
        
        <label for="dhcp_type">Select DHCP Version:</label>
        <select id="dhcp_type" name="dhcp_type">
            <option value="DHCPv4">DHCPv4</option>
            <option value="DHCPv6">DHCPv6</option>
        </select>

        <button type="submit">Request IP</button>
    </form>
</body>
</html>