-- ============================================================
-- SETUP TRACKING — Ejecutar UNA VEZ después de las migraciones
-- ============================================================

-- 1. Nuevos estados de vehículo (ct_estado_vehiculo es managed=False)
--    Verifica que IDs 1 y 2 ya existan; este script agrega del 3 al 7.
INSERT INTO ct_estado_vehiculo (id, estado) OVERRIDING SYSTEM VALUE VALUES
    (3, 'En Tránsito'),
    (4, 'En Aduana'),
    (5, 'En Preparación'),
    (6, 'Entregado'),
    (7, 'No Disponible')
ON CONFLICT (id) DO NOTHING;

-- 2. Estados del ciclo de vida del lote (ct_estado_lote es managed=True,
--    Django crea la tabla, pero los datos iniciales los insertamos aquí)
INSERT INTO ct_estado_lote (codigo, nombre, descripcion, orden, color_hex) VALUES
    ('PROGRAMADO',         'Programado',            'Orden de compra emitida, vehículos aún no fabricados.',        1,  '#6b7280'),
    ('EN_FABRICACION',     'En Fabricación',         'Fábrica en China confirma producción en curso.',               2,  '#f59e0b'),
    ('EMBARCADO',          'Embarcado',              'Contenedores cargados en el buque. BL generado.',              3,  '#3b82f6'),
    ('TRANSITO_MARITIMO',  'Tránsito Marítimo',      'En alta mar, en camino a Venezuela.',                          4,  '#06b6d4'),
    ('EN_ADUANA',          'En Aduana',              'Llegó al puerto venezolano, proceso aduanal en curso.',        5,  '#f97316'),
    ('EN_PUERTO',          'En Puerto',              'Liberado de aduana, en espera de transporte terrestre.',       6,  '#84cc16'),
    ('TRANSITO_NACIONAL',  'Tránsito Nacional',      'En camión hacia la sede de destino.',                          7,  '#a78bfa'),
    ('RECIBIDO_SEDE',      'Recibido en Sede',       'Llegó a la sede. Vehículos pasan a Disponible automáticamente.', 8, '#22c55e'),
    ('DISTRIBUIDO',        'Distribuido',            'Unidades distribuidas entre sedes para la venta.',             9,  '#10b981'),
    ('CERRADO',            'Cerrado',                'Todos los vehículos del lote fueron vendidos o transferidos.', 10, '#1f2937')
ON CONFLICT (codigo) DO NOTHING;

-- 3. Verificación rápida
SELECT 'ct_estado_vehiculo' AS tabla, COUNT(*) AS registros FROM ct_estado_vehiculo
UNION ALL
SELECT 'ct_estado_lote', COUNT(*) FROM ct_estado_lote;
