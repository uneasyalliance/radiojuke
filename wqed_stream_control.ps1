# $block = {& "C:\Program Files\VideoLAN\VLC\vlc.exe" "https://ice-1.streamhoster.com/lv_wqed--893" }
# startup cmd file in: C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp
$url = "https://ice-1.streamhoster.com/lv_wqed--893"

# could use this to check if mpv already running.
#$proc = Get-Process -name mpv -ErrorAction Silent

Write-Output "hello"
while ($true) {
	$rcvr_on = btdiscovery -n STR-DH190 -i1 -d"%c%"
	$start = (Get-Date)
	
	if (($rcvr_on -eq 'Yes' -and $job -eq $null) -and
		($start -gt "8:00" -and $start -lt "20:00"))
	{
		Write-Output "stream ON"
		Get-Date
		$job = Start-Job -scriptblock {& mpv $Using:url }
		Write-Output $job
	}
	elseif ($rcvr_on -eq 'No' -and $job -ne $null)
	{
		Write-Output $job
		Write-Output "stream OFF"
		Get-Date
		Stop-Job -id $job.id
		Remove-Job -id $job.id
		$job = $null
	}
}
Get-Job
Write-Output "bye"

