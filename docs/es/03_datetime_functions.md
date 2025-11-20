# Referencia de funciones de fecha y hora

[← Volver al índice de funciones integradas](00_index.md)

Referencia completa de las funciones de fecha y hora que se pueden usar en u5 EasyScripter.

## Lista de funciones
Se proporcionan 12 funciones de fecha y hora.

---

### NOW()
**Descripción**: Obtiene la fecha y hora actual
**Argumentos**: Ninguno
**Valor de retorno**: Cadena de fecha y hora (YYYY-MM-DD HH:MM:SS)
**Ejemplo**:
```vba
currentTime = NOW()
PRINT(currentTime)    ' "2024-01-15 14:30:45"
PRINT("Hora actual: " & NOW())
```

### DATE()
**Descripción**: Obtiene la fecha de hoy
**Argumentos**: Ninguno
**Valor de retorno**: Cadena de fecha (YYYY-MM-DD)
**Ejemplo**:
```vba
today = DATE()
PRINT(today)    ' "2024-01-15"
```

### TIME()
**Descripción**: Obtiene la hora actual
**Argumentos**: Ninguno
**Valor de retorno**: Cadena de hora (HH:MM:SS)
**Ejemplo**:
```vba
currentTime = TIME()
PRINT(currentTime)    ' "14:30:45"
```

### YEAR([date])
**Descripción**: Obtiene el año
**Argumentos**: date - Cadena de fecha (omitido: hoy)
**Valor de retorno**: Año (numérico)
**Ejemplo**:
```vba
result = YEAR()
PRINT(result)              ' 2024 (este año)
result = YEAR("2023-12-25")
PRINT(result)              ' 2023
```

### MONTH([date])
**Descripción**: Obtiene el mes
**Argumentos**: date - Cadena de fecha (omitido: hoy)
**Valor de retorno**: Mes (1-12)
**Ejemplo**:
```vba
result = MONTH()
PRINT(result)             ' 1 (mes actual)
result = MONTH("2023-12-25")
PRINT(result)             ' 12
```

### DAY([date])
**Descripción**: Obtiene el día
**Argumentos**: date - Cadena de fecha (omitido: hoy)
**Valor de retorno**: Día (1-31)
**Ejemplo**:
```vba
result = DAY()
PRINT(result)               ' 15 (hoy)
result = DAY("2023-12-25")
PRINT(result)               ' 25
```

### HOUR([time])
**Descripción**: Obtiene la hora
**Argumentos**: time - Cadena de hora (omitido: actual)
**Valor de retorno**: Hora (0-23)
**Ejemplo**:
```vba
result = HOUR()
PRINT(result)              ' 14 (hora actual)
result = HOUR("15:30:45")
PRINT(result)              ' 15
```

### MINUTE([time])
**Descripción**: Obtiene los minutos
**Argumentos**: time - Cadena de hora (omitido: actual)
**Valor de retorno**: Minutos (0-59)
**Ejemplo**:
```vba
result = MINUTE()
PRINT(result)            ' 30 (minutos actuales)
result = MINUTE("15:30:45")
PRINT(result)            ' 30
```

### SECOND([time])
**Descripción**: Obtiene los segundos
**Argumentos**: time - Cadena de hora (omitido: actual)
**Valor de retorno**: Segundos (0-59)
**Ejemplo**:
```vba
result = SECOND()
PRINT(result)            ' 45 (segundos actuales)
result = SECOND("15:30:45")
PRINT(result)            ' 45
```

### DATEADD(interval, number, [date])
**Descripción**: Suma/resta a fecha
**Argumentos**:
- interval - Unidad ("d"=día, "m"=mes, "y"=año, "h"=hora, "n"=minuto, "s"=segundo)
- number - Número a sumar
- date - Fecha y hora de referencia (omitido: actual)
**Valor de retorno**: Fecha y hora calculada (formato YYYY/MM/DD HH:MM:SS)
**Ejemplo**:
```vba
tomorrow = DATEADD("d", 1, DATE())
PRINT(tomorrow)        ' Mañana (ej: "2025/10/23 00:00:00")
nextMonth = DATEADD("m", 1, "2024-01-15")
PRINT(nextMonth)       ' "2024/02/15 00:00:00"
inOneHour = DATEADD("h", 1, NOW())
PRINT(inOneHour)       ' En una hora (ej: "2025/10/22 15:30:00")
```

### DATEDIFF(interval, date1, [date2])
**Descripción**: Calcula diferencia de fechas
**Argumentos**:
- interval - Unidad ("d"=día, "m"=mes, "y"=año, "h"=hora, "n"=minuto, "s"=segundo)
- date1 - Fecha y hora de inicio
- date2 - Fecha y hora de fin (omitido: actual)
**Valor de retorno**: Diferencia (numérico)
**Ejemplo**:
```vba
days = DATEDIFF("d", "2024-01-01", "2024-01-15")
PRINT(days)  ' 14
age = DATEDIFF("y", "1990-01-01", DATE())
PRINT(age)   ' Edad
hours = DATEDIFF("h", "2024-01-15 10:00:00", NOW())
PRINT(hours) ' Tiempo transcurrido
```

### CDATE(date_string)
**Descripción**: Convierte cadena de fecha a tipo de fecha (compatible con VBA)
**Argumentos**: date_string - Cadena que representa una fecha
**Valor de retorno**: Cadena de fecha (formato YYYY/MM/DD HH:MM:SS)
**Formatos flexibles admitidos**:
- Fecha y hora completa: `"2025/11/05 15:39:49"` → `2025/11/05 15:39:49`
- Solo fecha: `"2025/11/05"` → `2025/11/05 00:00:00` (hora es 00:00:00)
- Solo año y mes: `"2025/11"` → `2025/11/01 00:00:00` (día=1, hora=00:00:00)
- Solo año: `"2025"` → `2025/01/01 00:00:00` (mes día=1/1, hora=00:00:00)

**Ejemplo**:
```vba
' Fecha y hora completa
result = CDATE("2025/11/05 15:39:49")
PRINT(result)  ' "2025/11/05 15:39:49"

' Solo fecha (hora se convierte en 00:00:00)
result = CDATE("2025/11/05")
PRINT(result)  ' "2025/11/05 00:00:00"

' Fecha parcial (parte faltante se complementa)
result = CDATE("2025/11")
PRINT(result)  ' "2025/11/01 00:00:00"
```

---

[← Volver al índice de funciones integradas](00_index.md)
