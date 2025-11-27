# BGH ERP Management Script
# Quick commands for managing the ERP system

# Start development server
function Start-ERPServer {
    Write-Host "Starting BGH ERP Development Server..." -ForegroundColor Green
    python manage.py runserver
}

# Create superuser
function New-ERPAdmin {
    Write-Host "Creating new admin user..." -ForegroundColor Green
    python manage.py createsuperuser
}

# Run migrations
function Update-ERPDatabase {
    Write-Host "Running migrations..." -ForegroundColor Green
    python manage.py makemigrations
    python manage.py migrate
}

# Run tests
function Test-ERP {
    Write-Host "Running tests..." -ForegroundColor Green
    python manage.py test
}

# Create backup
function Backup-ERPDatabase {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupFile = "backup_$timestamp.json"
    Write-Host "Creating backup: $backupFile" -ForegroundColor Green
    python manage.py dumpdata > $backupFile
    Write-Host "Backup created successfully!" -ForegroundColor Green
}

# Restore backup
function Restore-ERPDatabase {
    param([string]$BackupFile)
    if (Test-Path $BackupFile) {
        Write-Host "Restoring from backup: $BackupFile" -ForegroundColor Yellow
        python manage.py loaddata $BackupFile
        Write-Host "Restore completed!" -ForegroundColor Green
    } else {
        Write-Host "Backup file not found: $BackupFile" -ForegroundColor Red
    }
}

# Show all available commands
function Show-ERPCommands {
    Write-Host "`nBGH ERP Available Commands:" -ForegroundColor Cyan
    Write-Host "  Start-ERPServer        - Start development server" -ForegroundColor Yellow
    Write-Host "  New-ERPAdmin           - Create admin user" -ForegroundColor Yellow
    Write-Host "  Update-ERPDatabase     - Run migrations" -ForegroundColor Yellow
    Write-Host "  Test-ERP               - Run tests" -ForegroundColor Yellow
    Write-Host "  Backup-ERPDatabase     - Create database backup" -ForegroundColor Yellow
    Write-Host "  Restore-ERPDatabase    - Restore from backup" -ForegroundColor Yellow
    Write-Host "`n"
}

# Display welcome message
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   BGH ERP Management Console" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan
Show-ERPCommands
