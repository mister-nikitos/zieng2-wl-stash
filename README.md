# Подписка для обхода белых списков от zieng2 - Версия для Stash

[![Update](https://github.com/mister-nikitos/zieng2-wl-stash/actions/workflows/update.yml/badge.svg)](https://github.com/mister-nikitos/zieng2-wl-stash/actions/workflows/update.yml)

Автоматический конвертер списков VLESS-прокси из [zieng2/wl](https://github.com/zieng2/wl) в формат [Stash](https://stash.wiki) proxy provider. Обновляется каждый час через GitHub Actions.

## Ссылки подписки

| Вариант | Регион | Описание | Ссылка |
|---|---|---|---|
| **Lite** (рекомендуемый) | Все | Прокси из проверенных подсетей — более надёжные и стабильные | `https://raw.githubusercontent.com/mister-nikitos/zieng2-wl-stash/main/output/stash_lite.yaml` |
| **Lite RU** | `ru` | Lite-подборка только для прокси с меткой `🇷🇺` в названии | `https://raw.githubusercontent.com/mister-nikitos/zieng2-wl-stash/main/output/stash_lite_ru.yaml` |
| **Lite Global** | `global` | Lite-подборка для всех прокси без метки `🇷🇺` | `https://raw.githubusercontent.com/mister-nikitos/zieng2-wl-stash/main/output/stash_lite_global.yaml` |
| **Universal** | Все | Все найденные прокси — максимальный выбор, но часть может быть нестабильна | `https://raw.githubusercontent.com/mister-nikitos/zieng2-wl-stash/main/output/stash_universal.yaml` |
| **Universal RU** | `ru` | Полная RU-подборка по метке `🇷🇺` в названии | `https://raw.githubusercontent.com/mister-nikitos/zieng2-wl-stash/main/output/stash_universal_ru.yaml` |
| **Universal Global** | `global` | Полная Global-подборка для всех прокси без метки `🇷🇺` | `https://raw.githubusercontent.com/mister-nikitos/zieng2-wl-stash/main/output/stash_universal_global.yaml` |

`lite` и `universal` определяют объём и качество исходной выборки. `ru` и `global` определяются только по метке в названии прокси: если в имени есть `🇷🇺`, прокси попадает в `ru`, иначе — в `global`. Это деление не использует IP-геолокацию или проверку фактической страны сервера.

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

При желании можно заменить URL на `.../stash_lite_ru.yaml`, `.../stash_lite_global.yaml`, `.../stash_universal_ru.yaml` или `.../stash_universal_global.yaml`.

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
