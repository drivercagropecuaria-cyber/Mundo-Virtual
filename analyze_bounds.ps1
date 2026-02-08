$json = Get-Content 'Villa_Canabrava_Digital_World/data/final_export/VILLA_CANABRAVA_DIGITAL_TWIN_GOLDEN.geojson' | ConvertFrom-Json
$lons = @()
$lats = @()

foreach ($feature in $json.features) {
  if ($feature.geometry.coordinates) {
    if ($feature.geometry.type -eq 'Polygon') {
      foreach ($ring in $feature.geometry.coordinates) {
        foreach ($point in $ring) {
          $lons += $point[0]
          $lats += $point[1]
        }
      }
    } elseif ($feature.geometry.type -eq 'LineString') {
      foreach ($point in $feature.geometry.coordinates) {
        $lons += $point[0]
        $lats += $point[1]
      }
    }
  }
}

if ($lons.Count -gt 0) {
  $minLon = ($lons | Measure-Object -Minimum).Minimum
  $maxLon = ($lons | Measure-Object -Maximum).Maximum
  $minLat = ($lats | Measure-Object -Minimum).Minimum
  $maxLat = ($lats | Measure-Object -Maximum).Maximum
  $centerLon = ($minLon + $maxLon) / 2
  $centerLat = ($minLat + $maxLat) / 2
  
  Write-Host "GeoJSON Bounds (VILLA_CANABRAVA_DIGITAL_TWIN_GOLDEN.geojson):"
  Write-Host "  Min Latitude: $minLat"
  Write-Host "  Max Latitude: $maxLat"
  Write-Host "  Min Longitude: $minLon"
  Write-Host "  Max Longitude: $maxLon"
  Write-Host "  Centróide: $centerLon, $centerLat"
} else {
  Write-Host "Nenhuma coordenada encontrada"
}
