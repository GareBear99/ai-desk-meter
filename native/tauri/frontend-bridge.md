# Frontend Bridge

The dashboard shell should use the same API contract as the browser dashboard.

## Health check

```js
const health = await fetch('http://127.0.0.1:8787/health').then(r => r.json())
```

## Provider status

```js
const provider = 'mock'
const status = await fetch(`http://127.0.0.1:8787/status?provider=${provider}`).then(r => r.json())
```

## Companion payload preview

```js
const compact = await fetch(`http://127.0.0.1:8787/companion/status?provider=${provider}`).then(r => r.json())
```

## UI states

Render provider-reported states exactly: linked, offline, stale, warning, error, timeout, and invalid backend output. The frontend should not replace backend errors with fake success states.
