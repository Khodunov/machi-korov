# Пивной ларёк — версия 2

Десять сюжетов перегенерированы встроенным image_gen в более реалистичной рисованной манере: естественные пропорции людей, сдержанные лица, тонкий контур, матовая гуашь и приглушённые цвета. Визуальные ориентиры — исходный пивной ларёк и обновлённая панелька с ковром.

[Все иллюстрации](cards/pivnye-larki-v2-ten-art.jpg) · [Все карты](cards/pivnye-larki-v2-ten-cards.jpg)

| Сюжет | Исходник на белом | Прозрачный PNG | Карта |
|---|---|---|---|
| А вот ту жвачку! | [PNG](buildings/pivnoy-laryok-01-zhvachka-v2-source.png) | [PNG](buildings/pivnoy-laryok-01-zhvachka-v2.png) | [PNG](cards/pivnoy-laryok-01-zhvachka-v2.png) |
| По одной — и домой | [PNG](buildings/pivnoy-laryok-02-domoy-v2-source.png) | [PNG](buildings/pivnoy-laryok-02-domoy-v2.png) | [PNG](cards/pivnoy-laryok-02-domoy-v2.png) |
| Под козырьком | [PNG](buildings/pivnoy-laryok-03-kozyrek-v2-source.png) | [PNG](buildings/pivnoy-laryok-03-kozyrek-v2.png) | [PNG](cards/pivnoy-laryok-03-kozyrek-v2.png) |
| Тропа народная | [PNG](buildings/pivnoy-laryok-04-tropa-v2-source.png) | [PNG](buildings/pivnoy-laryok-04-tropa-v2.png) | [PNG](cards/pivnoy-laryok-04-tropa-v2.png) |
| Большой футбол | [PNG](buildings/pivnoy-laryok-05-futbol-v2-source.png) | [PNG](buildings/pivnoy-laryok-05-futbol-v2.png) | [PNG](cards/pivnoy-laryok-05-futbol-v2.png) |
| Островок торговли | [PNG](buildings/pivnoy-laryok-06-ostrovok-v2-source.png) | [PNG](buildings/pivnoy-laryok-06-ostrovok-v2.png) | [PNG](cards/pivnoy-laryok-06-ostrovok-v2.png) |
| Без сдачи | [PNG](buildings/pivnoy-laryok-07-bez-sdachi-v2-source.png) | [PNG](buildings/pivnoy-laryok-07-bez-sdachi-v2.png) | [PNG](cards/pivnoy-laryok-07-bez-sdachi-v2.png) |
| На минутку | [PNG](buildings/pivnoy-laryok-08-minutka-v2-source.png) | [PNG](buildings/pivnoy-laryok-08-minutka-v2.png) | [PNG](cards/pivnoy-laryok-08-minutka-v2.png) |
| Рыбный инспектор | [PNG](buildings/pivnoy-laryok-09-kot-v2-source.png) | [PNG](buildings/pivnoy-laryok-09-kot-v2.png) | [PNG](cards/pivnoy-laryok-09-kot-v2.png) |
| Последний покупатель | [PNG](buildings/pivnoy-laryok-10-novyy-god-v2-source.png) | [PNG](buildings/pivnoy-laryok-10-novyy-god-v2.png) | [PNG](cards/pivnoy-laryok-10-novyy-god-v2.png) |

Предыдущие версии сохранены. Каждый сюжет генерировался отдельным запросом. Белый фон удалён локально; внутренние просветы между ветками дочищены по маскам.

Промпты: `prompts/central-illustrations/pivnye-larki-v2-generation-records.json`.

Повторная обработка и сборка:

```sh
.venv/bin/python scripts/render_pivnye_larki_v2.py
```

В варианте 6 рекламный плакат убран локальным клонированием фактуры металлической стены после повторных сетевых ошибок image_gen. Исходник сохранён без этой ретуши; прозрачный PNG и карта содержат исправление.
