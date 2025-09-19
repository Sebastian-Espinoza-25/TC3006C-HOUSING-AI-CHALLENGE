# API de Preferencias Específicas

## Endpoint
```
POST /api/clients/{client_id}/preferences/specific
```

## Descripción
Este endpoint permite crear o actualizar preferencias específicas del cliente utilizando únicamente los campos de la lista proporcionada y mapeando automáticamente campos del JSON de predicción de IA.

## Campos Soportados

### Campos Directos de Preferencias
La ruta acepta los siguientes campos directamente:

1. `preferred_neighborhood` (VARCHAR(100))
2. `preferred_condition1` (VARCHAR(20))
3. `preferred_house_style` (VARCHAR(20))
4. `min_year_built` (INT)
5. `max_year_built` (INT)
6. `min_lot_area` (FLOAT)
7. `max_lot_area` (FLOAT)
8. `min_lot_frontage` (FLOAT)
9. `max_lot_frontage` (FLOAT)
10. `min_1st_flr_sf` (FLOAT)
11. `max_1st_flr_sf` (FLOAT)
12. `min_2nd_flr_sf` (FLOAT)
13. `max_2nd_flr_sf` (FLOAT)
14. `min_gr_liv_area` (FLOAT)
15. `max_gr_liv_area` (FLOAT)
16. `min_bedroom_abv_gr` (INT)
17. `max_bedroom_abv_gr` (INT)
18. `min_kitchen_abv_gr` (INT)
19. `max_kitchen_abv_gr` (INT)
20. `min_tot_rms_abv_grd` (INT)
21. `max_tot_rms_abv_grd` (INT)
22. `min_full_bath` (INT)
23. `max_full_bath` (INT)
24. `min_half_bath` (INT)
25. `max_half_bath` (INT)
26. `preferred_heating_qc` (VARCHAR(20))
27. `min_fireplaces` (INT)
28. `max_fireplaces` (INT)
29. `min_garage_cars` (INT)
30. `max_garage_cars` (INT)
31. `min_garage_area` (FLOAT)
32. `max_garage_area` (FLOAT)
33. `min_wood_deck_sf` (FLOAT)
34. `max_wood_deck_sf` (FLOAT)
35. `min_open_porch_sf` (FLOAT)
36. `max_open_porch_sf` (FLOAT)
37. `min_enclosed_porch` (FLOAT)
38. `max_enclosed_porch` (FLOAT)
39. `preferred_fence` (VARCHAR(20))
40. `min_sale_price` (FLOAT)
41. `max_sale_price` (FLOAT)
42. `preferred_sale_type` (VARCHAR(20))

### Mapeo Automático de JSON de Predicción
El endpoint también mapea automáticamente los siguientes campos del JSON de predicción de IA:

| Campo JSON | Campo de Preferencia | Descripción |
|------------|---------------------|-------------|
| `Neighborhood` | `preferred_neighborhood` | Barrio preferido |
| `YearBuilt` | `min_year_built` y `max_year_built` | Año de construcción (mismo valor para min y max) |
| `LotArea` | `min_lot_area` y `max_lot_area` | Área del lote (mismo valor para min y max) |
| `1stFlrSF` | `min_1st_flr_sf` y `max_1st_flr_sf` | Área del primer piso (mismo valor para min y max) |
| `2ndFlrSF` | `min_2nd_flr_sf` y `max_2nd_flr_sf` | Área del segundo piso (mismo valor para min y max) |
| `GrLivArea` | `min_gr_liv_area` y `max_gr_liv_area` | Área habitable total (mismo valor para min y max) |
| `Fireplaces` | `min_fireplaces` y `max_fireplaces` | Número de chimeneas (mismo valor para min y max) |
| `GarageCars` | `min_garage_cars` y `max_garage_cars` | Número de carros en garaje (mismo valor para min y max) |
| `GarageArea` | `min_garage_area` y `max_garage_area` | Área del garaje (mismo valor para min y max) |
| `SaleCondition` | `preferred_sale_type` | Tipo de venta preferido |

## Ejemplos de Uso

### Ejemplo 1: Campos Directos
```json
POST /api/clients/1/preferences/specific
{
    "preferred_neighborhood": "NridgHt",
    "preferred_condition1": "Norm",
    "min_year_built": 2000,
    "max_year_built": 2010,
    "min_lot_area": 10000.0,
    "max_lot_area": 15000.0,
    "min_gr_liv_area": 1500.0,
    "max_gr_liv_area": 2000.0,
    "min_bedroom_abv_gr": 3,
    "max_bedroom_abv_gr": 4,
    "min_sale_price": 200000.0,
    "max_sale_price": 300000.0
}
```

### Ejemplo 2: JSON de Predicción de IA
```json
POST /api/clients/1/preferences/specific
{
    "TotalSF": 3616.0,
    "OverallQual": 8.0,
    "OverallCond": 5.0,
    "GrLivArea": 1822.0,
    "Neighborhood": "NridgHt",
    "TotalBath": 5.0,
    "LotArea": 14122.0,
    "CentralAir": "Y",
    "YearBuilt": 2005.0,
    "RemodAge": 5.0,
    "YearRemodAdd": 2006.0,
    "1stFlrSF": 1822.0,
    "HouseAge": 5.0,
    "GarageArea": 678.0,
    "GarageScore": 2034.0,
    "BsmtFinSF1": 28.0,
    "SaleCondition": "Normal",
    "TotalPorchSF": 119.0,
    "GarageCars": 3.0,
    "2ndFlrSF": 0.0,
    "Fireplaces": 1.0,
    "RoomsPlusBathEq": 11.5
}
```

### Ejemplo 3: Datos Mixtos
```json
POST /api/clients/1/preferences/specific
{
    "preferred_neighborhood": "NridgHt",
    "min_sale_price": 250000.0,
    "max_sale_price": 350000.0,
    "Neighborhood": "NridgHt",
    "YearBuilt": 2005.0,
    "LotArea": 14122.0,
    "GrLivArea": 1822.0,
    "Fireplaces": 1.0,
    "GarageCars": 3.0,
    "GarageArea": 678.0,
    "SaleCondition": "Normal"
}
```

## Respuestas

### Éxito (201)
```json
{
    "message": "Preferencias específicas creadas/actualizadas correctamente",
    "preferences": {
        "preference_id": 1,
        "client_id": 1,
        "preferred_neighborhood": "NridgHt",
        "min_year_built": 2005,
        "max_year_built": 2005,
        "min_lot_area": 14122.0,
        "max_lot_area": 14122.0,
        // ... otros campos
    },
    "mapped_fields": [
        "preferred_neighborhood",
        "min_year_built",
        "max_year_built",
        "min_lot_area",
        "max_lot_area"
        // ... otros campos mapeados
    ]
}
```

### Error - Cliente no encontrado (404)
```json
{
    "error": "Cliente no encontrado"
}
```

### Error - Sin campos válidos (400)
```json
{
    "error": "No se proporcionaron campos válidos para las preferencias"
}
```

### Error del servidor (500)
```json
{
    "error": "Mensaje de error específico"
}
```

## Notas Importantes

1. **Campos Opcionales**: Todos los campos son opcionales. El endpoint acepta cualquier combinación de los campos soportados.

2. **Mapeo Automático**: Los campos del JSON de predicción se mapean automáticamente a los campos de preferencias correspondientes.

3. **Valores Min/Max**: Para campos numéricos del JSON, el mismo valor se usa tanto para `min_` como `max_` para crear un rango exacto.

4. **Actualización**: Si el cliente ya tiene preferencias, se actualizarán. Si no las tiene, se crearán nuevas.

5. **Validación**: El endpoint valida que al menos se proporcione un campo válido antes de procesar la solicitud.

## Pruebas

Para probar el endpoint, puedes usar el archivo `test_specific_preferences.py` incluido en el proyecto:

```bash
python test_specific_preferences.py
```

Asegúrate de que el servidor esté ejecutándose y de que exista un cliente con el ID especificado en el script de prueba.
