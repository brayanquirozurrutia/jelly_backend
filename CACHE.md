# Documentación del Caché en la Aplicación

## Introducción

La aplicación utiliza caché para optimizar el rendimiento y reducir la carga en la base de datos. A continuación se describe la configuración del caché, las claves utilizadas, y cómo se manejan.

---

## Claves de Caché y Datos Asociados

### Clave: `banner_phrases`

- **Descripción**: Lista de todas las frases de banner.
- **Tipo de Datos**: Lista de objetos `BannerPhrase`.
- **Tiempo de Expiración**: 1 hora (3600 segundos).
- **Uso**: Se utiliza para proporcionar una lista de todas las frases de banner en la consulta GraphQL.

### Clave: `banner_phrase_<phrase>`

- **Descripción**: Indica si una frase específica ya está en la base de datos.
- **Tipo de Datos**: Booleano (`True` o `False`).
- **Tiempo de Expiración**: Variable (se expira cuando se actualiza o elimina la frase).
- **Uso**: Se utiliza para verificar si una frase ya existe antes de agregar una nueva.

### Clave: `banner_phrase_count`

- **Descripción**: Número total de frases de banner almacenadas.
- **Tipo de Datos**: Entero.
- **Tiempo de Expiración**: 1 hora (3600 segundos).
- **Uso**: Controla el límite de frases de banner permitidas (máximo de 10).

---

## Estrategias de Invalidez y Actualización

### Crear una Frase de Banner

- **Acción**: Cuando se agrega una nueva frase de banner, se verifica si el número total de frases excede el límite permitido.
- **Invalida**: Se elimina la clave `banner_phrases` para forzar una actualización en la próxima consulta.

### Actualizar una Frase de Banner

- **Acción**: Se elimina la clave `banner_phrase_<old_phrase>` y se actualiza la clave `banner_phrase_<new_phrase>`.
- **Invalida**: La clave `banner_phrases` se elimina para forzar una actualización en la próxima consulta.

### Eliminar una Frase de Banner

- **Acción**: Se elimina la clave `banner_phrase_<phrase>`.
- **Invalida**: La clave `banner_phrases` y `banner_phrase_count` se actualizan para reflejar el cambio.

---

## Ejemplos de Uso

### Consulta de Frases de Banner en GraphQL

```graphql
query {
  bannerPhrases {
    id
    phrase
  }
}
```
