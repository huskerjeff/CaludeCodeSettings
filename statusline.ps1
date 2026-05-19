param()

$ErrorActionPreference = 'SilentlyContinue'

# Read JSON input from stdin
$input_json = [Console]::In.ReadToEnd()
$data = $input_json | ConvertFrom-Json

# Model
$model = $data.model.display_name
if (-not $model) { $model = "Claude" }

# Tokens — sum input+output from latest assistant message usage in transcript
$tok_str = "-- tok"
$ctx_str = "--"
try {
    $transcript = $data.transcript_path
    if ($transcript -and (Test-Path $transcript)) {
        $total = 0
        $lines = Get-Content $transcript -Tail 200
        foreach ($line in $lines) {
            try {
                $obj = $line | ConvertFrom-Json
                if ($obj.message.usage) {
                    $u = $obj.message.usage
                    $t = [int]$u.input_tokens + [int]$u.cache_read_input_tokens + [int]$u.cache_creation_input_tokens + [int]$u.output_tokens
                    if ($t -gt $total) { $total = $t }
                }
            } catch {}
        }
        if ($total -gt 0) {
            $tok_str = "{0:N1}k tok" -f ($total / 1000)
            $pct = [math]::Round(($total / 200000) * 100)
            $ctx_str = "$pct%"
        }
    }
} catch {}

# Time
$time = (Get-Date).ToString("HH:mm:ss")

# CPU
$cpu = "--"
try {
    $cpu_val = (Get-CimInstance Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average
    $cpu = "$([int]$cpu_val)%"
} catch {}

# Memory used (GB)
$mem = "--"
try {
    $os = Get-CimInstance Win32_OperatingSystem
    $used_gb = ($os.TotalVisibleMemorySize - $os.FreePhysicalMemory) / 1MB
    $mem = "{0:N1}G" -f $used_gb
} catch {}

# Battery
$bat = "--"
try {
    $b = Get-CimInstance Win32_Battery
    if ($b) {
        $pct = $b.EstimatedChargeRemaining
        $charging = if ($b.BatteryStatus -eq 2 -or $b.BatteryStatus -eq 6 -or $b.BatteryStatus -eq 7 -or $b.BatteryStatus -eq 8 -or $b.BatteryStatus -eq 9) { "+" } else { "" }
        $bat = "$pct%$charging"
    } else {
        $bat = "AC"
    }
} catch {}

# ANSI colors
$e = [char]27
$cyan    = "$e[36m"
$gray    = "$e[90m"
$yellow  = "$e[33m"
$green   = "$e[32m"
$magenta = "$e[35m"
$reset   = "$e[0m"
$sep     = "$gray|$reset"

Write-Output "$cyan$model$reset $sep ctx: $ctx_str $sep $yellow$tok_str$reset $sep $green$time$reset $sep $magenta cpu:$cpu mem:$mem bat:$bat$reset"
