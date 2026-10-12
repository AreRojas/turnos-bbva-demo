# Turnos de sucursal

Demo académica inspirada en la experiencia visual de BBVA, con frontend Angular y API Flask.

## Funciones

- Generación de turnos consecutivos A01, A02, A03…
- Cuatro ventanillas con llamada manual del siguiente turno.
- Al finalizar una atención, la ventanilla toma el siguiente turno y lo anuncia en pantalla con un sonido breve.
- Panel de espera y estadísticas.

## Desarrollo local

Requisitos: Node.js 20.19+ y Python 3.10+.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m flask --app api.index run --port 5000
```

En otra terminal:

```powershell
npm install
npm start
```

El proxy Angular incluido reenvía `/api` a `http://127.0.0.1:5000`.

## Publicación

El proyecto configura `/api` como función Python de Vercel y el resto como frontend estático Angular. La cola está en memoria para demostración; en despliegues serverless los datos no son persistentes ni se comparten necesariamente entre instancias. Para uso real, conectar una base de datos compartida.

```sh
npm install
npm run build
vercel
```

Conecta el repositorio a Vercel para que los cambios publicados en Git activen despliegues automáticos.
