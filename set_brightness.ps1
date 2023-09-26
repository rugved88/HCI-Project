param([int]$brightness)

$monitor = Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods
$monitor.WmiSetBrightness(1, $brightness)