# Подписка для обхода белых списков от zieng2 - Версия для Stash

[![Update](https://github.com/mister-nikitos/zieng2-wl-stash/actions/workflows/update.yml/badge.svg)](https://github.com/mister-nikitos/zieng2-wl-stash/actions/workflows/update.yml)

Автоматический конвертер списков VLESS-прокси из [zieng2/wl](https://github.com/zieng2/wl) в формат [Stash](https://stash.wiki) proxy provider. Обновляется каждый час через GitHub Actions.

## Ссылки подписки

| Вариант | Описание | Ссылка |
|---|---|---|
| **Lite** (рекомендуемый) | Прокси из проверенных подсетей — более надёжные и стабильные | `https://raw.githubusercontent.com/mister-nikitos/zieng2-wl-stash/main/output/stash_lite.yaml` |
| **Universal** | Все найденные прокси — максимальный выбор, но часть может быть нестабильна | `https://raw.githubusercontent.com/mister-nikitos/zieng2-wl-stash/main/output/stash_universal.yaml` |

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

## Поддерживаемые типы безопасности

| Безопасность | Статус |
|---|---|
| None | ✅ |
| TLS | ✅ |
| REALITY | ✅ |
| XTLS (flow) | ✅ |

## Источник

Данные берутся из проекта [zieng2/wl](https://github.com/zieng2/wl), который обновляется раз в час.
