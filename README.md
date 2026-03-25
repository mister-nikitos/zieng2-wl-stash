# zieng2-wl-stash

Автоматический конвертер списков VLESS-прокси из [zieng2/wl](https://github.com/zieng2/wl) в формат [Stash](https://stash.wiki) proxy provider. Обновляется каждый час через GitHub Actions.

## Ссылки подписки

| Вариант | Описание | Ссылка |
|---|---|---|
| **Lite** (рекомендуемый) | Проверенные подсети | `https://raw.githubusercontent.com/mister-nikitos/zieng2-wl-stash/main/output/stash_lite.yaml` |
| **Universal** | Все доступные подсети | `https://raw.githubusercontent.com/mister-nikitos/zieng2-wl-stash/main/output/stash_universal.yaml` |

## Использование в Stash

Добавьте в ваш конфиг Stash:

```yaml
proxy-providers:
  zieng2-lite:
    url: https://raw.githubusercontent.com/mister-nikitos/zieng2-wl-stash/main/output/stash_lite.yaml
    interval: 3600

proxy-groups:
  - name: Proxy
    type: select
    use:
      - zieng2-lite
```

## Поддерживаемые транспорты

| Транспорт | Статус |
|---|---|
| TCP | ✅ |
| WebSocket | ✅ |
| gRPC | ✅ |
| H2 | ✅ |
| xHTTP | ❌ (не поддерживается Stash) |

## Источник

Данные берутся из проекта [zieng2/wl](https://github.com/zieng2/wl), который обновляется раз в час.
