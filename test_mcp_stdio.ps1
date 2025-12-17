# Test script for MCP stdio mode

Write-Host "=== Testing MCP Stdio Mode ===" -ForegroundColor Green
Write-Host ""

# Start the MCP server
$process = Start-Process python -ArgumentList "-m", "mcp_home_simulator", "--mcp" -NoNewWindow -PassThru -RedirectStandardInput ".\test_input.json" -RedirectStandardOutput ".\test_output.json" -RedirectStandardError ".\test_error.json"

# Wait for the process to start
Start-Sleep -Seconds 2

# Stop the process
Stop-Process -Id $process.Id -Force

Write-Host "Output:" -ForegroundColor Yellow
Get-Content ".\test_output.json" -ErrorAction SilentlyContinue | ForEach-Object { Write-Host $_ }

Write-Host ""
Write-Host "Done!" -ForegroundColor Green
