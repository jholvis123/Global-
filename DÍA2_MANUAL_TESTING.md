# DÍA 2 - PRUEBAS E2E EN NAVEGADOR
## Manual de Testing: Frontend → Backend → Database

### 📋 CHECKLIST DE PRUEBAS MANUALES

#### PARTE 1: INTERFAZ Y CARGA
- [ ] 1. Acceder a `http://localhost:4200`
- [ ] 2. Verificar que la página carga sin errores (console vacía)
- [ ] 3. Ver componente de chatbot visible
- [ ] 4. Verificar Material Design theme cargada (colores, iconos)

#### PARTE 2: VALIDACIÓN DE FORMULARIO
- [ ] 5. Click en campo "mensaje" - debe estar vacío
- [ ] 6. Intentar enviar con campo vacío - botón debe estar deshabilitado
- [ ] 7. Escribir menos de 10 caracteres - botón deshabilitado
- [ ] 8. Escribir más de 10 caracteres - botón habilitado

#### PARTE 3: COTIZACIONES EXITOSAS
**Test 3A: Cotización Básica**
```
Mensaje: "Necesito 500 kilos desde Santa Cruz a La Paz"
Esperado:
  ✓ Origen: Santa Cruz
  ✓ Destino: La Paz
  ✓ Peso: 500 kg
  ✓ Tipo: general
  ✓ Precio: 650 Bs
```
- [ ] 9. Enviar mensaje 3A
- [ ] 10. Ver respuesta dentro de 1-2 segundos
- [ ] 11. Verificar que los datos coinciden

**Test 3B: Carga Peligrosa**
```
Mensaje: "2 toneladas carga peligrosa Santa Cruz a Cochabamba"
Esperado:
  ✓ Peso: 2000 kg (convertido de toneladas)
  ✓ Tipo: peligrosa
  ✓ Precio: 2700 Bs
```
- [ ] 12. Enviar mensaje 3B
- [ ] 13. Verificar conversión de toneladas
- [ ] 14. Verificar tipo_carga correcto

**Test 3C: Carga Refrigerada**
```
Mensaje: "1500 kg refrigerado La Paz para Cochabamba"
Esperado:
  ✓ Tipo: refrigerada
  ✓ Precio: 1300 Bs
```
- [ ] 15. Enviar mensaje 3C
- [ ] 16. Verificar que tipo se detectó

#### PARTE 4: MANEJO DE ERRORES
**Test 4A: Sin Destino**
```
Mensaje: "500 kg desde La Paz"
Esperado: Mensaje de error amigable
```
- [ ] 17. Enviar mensaje 4A
- [ ] 18. Verificar que show error message, NOT crash

**Test 4B: Ruta No Disponible**
```
Mensaje: "100 kg Beni a Pando"
Esperado: Mensaje de error "No cubrimos esa ruta"
```
- [ ] 19. Enviar mensaje 4B
- [ ] 20. Verificar error message

#### PARTE 5: HISTORIAL Y ESTADO
- [ ] 21. Verificar que múltiples cotizaciones se muestran en lista
- [ ] 22. Cada cotización tiene ID único
- [ ] 23. Fechas mostradas en formato legible
- [ ] 24. Posibilidad de "limpiar historial" (si existe)

#### PARTE 6: RESPONSIVIDAD
- [ ] 25. Abrir DevTools (F12)
- [ ] 26. Toggle device toolbar (Ctrl+Shift+M)
- [ ] 27. Probar en Mobile (375px width)
- [ ] 28. Probar en Tablet (768px width)
- [ ] 29. Probar en Desktop (1920px width)
- [ ] 30. Verificar que todo es responsive

#### PARTE 7: RENDIMIENTO
- [ ] 31. Abrir Network tab en DevTools
- [ ] 32. Usar "Slow 3G" throttling
- [ ] 33. Hacer una cotización
- [ ] 34. Verificar request al backend
- [ ] 35. Verificar response time < 2s

#### PARTE 8: PERSISTENCIA EN BD
- [ ] 36. Hacer 3 cotizaciones diferentes
- [ ] 37. Cada una debe tener ID único creciente
- [ ] 38. Refresh página (F5)
- [ ] 39. Historial debe persists (si se cargan del backend)

---

## RESULTADO ESPERADO
✓ Todos los pasos completados sin errores  
✓ Mensajes claros en español  
✓ No hay excepciones en console  
✓ API responde en < 100ms  
✓ Frontend se renderiza en < 2s  

## COMANDOS ÚTILES PARA DEBUG

### Ver logs en console:
```javascript
// En Console de DevTools
localStorage.clear()  // Limpiar estado
fetch('http://localhost:8000/api/v1/chatbot/health').then(r => r.json()).then(d => console.log(d))
```

### Verificar BD desde terminal:
```bash
cd backend
python -c "
from app.db.database import SessionLocal
from app.domain.chatbot.entities import SolicitudCotizacion
db = SessionLocal()
solicitudes = db.query(SolicitudCotizacion).order_by(SolicitudCotizacion.id.desc()).limit(5).all()
for s in solicitudes:
    print(f'ID: {s.id} | {s.origen} → {s.destino} | {s.peso_kg}kg | \${s.precio_calculado}bs')
db.close()
"
```

## NOTAS
- Si algún test falla, revisar console (F12)
- Si error 404: Verificar puertos 8000 y 4200
- Si error CORS: Revisar backend CORS configuration
- Si respuestas lentas: Verificar load en backend terminal
