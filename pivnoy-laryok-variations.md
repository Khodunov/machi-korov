# Пивной ларёк — десять сюжетов

Созданы встроенным image_gen отдельными запросами на обычном белом фоне. Фон удалён локально. Исходники сохранены отдельно от прозрачных PNG.

Общие визуальные ориентиры: исходный ларёк и панелька с ковром; серый старый киоск, плотные цветные витрины, мультяшные персонажи с выразительными лицами.

[Обзор иллюстраций](cards/pivnye-larki-ten-art.jpg) · [Обзор карт](cards/pivnye-larki-ten-cards.jpg)

| № | Сюжет | Исходник | Прозрачный PNG | Карта |
|---|---|---|---|---|
| 1 | А вот ту жвачку! | [PNG](buildings/pivnoy-laryok-01-zhvachka-source.png) | [PNG](buildings/pivnoy-laryok-01-zhvachka.png) | [PNG](cards/pivnoy-laryok-01-zhvachka.png) |
| 2 | По одной — и домой | [PNG](buildings/pivnoy-laryok-02-domoy-source.png) | [PNG](buildings/pivnoy-laryok-02-domoy.png) | [PNG](cards/pivnoy-laryok-02-domoy.png) |
| 3 | Под козырьком | [PNG](buildings/pivnoy-laryok-03-kozyrek-source.png) | [PNG](buildings/pivnoy-laryok-03-kozyrek.png) | [PNG](cards/pivnoy-laryok-03-kozyrek.png) |
| 4 | Тропа народная | [PNG](buildings/pivnoy-laryok-04-tropa-source.png) | [PNG](buildings/pivnoy-laryok-04-tropa.png) | [PNG](cards/pivnoy-laryok-04-tropa.png) |
| 5 | Большой футбол | [PNG](buildings/pivnoy-laryok-05-futbol-source.png) | [PNG](buildings/pivnoy-laryok-05-futbol.png) | [PNG](cards/pivnoy-laryok-05-futbol.png) |
| 6 | Островок торговли | [PNG](buildings/pivnoy-laryok-06-ostrovok-source.png) | [PNG](buildings/pivnoy-laryok-06-ostrovok.png) | [PNG](cards/pivnoy-laryok-06-ostrovok.png) |
| 7 | Без сдачи | [PNG](buildings/pivnoy-laryok-07-bez-sdachi-source.png) | [PNG](buildings/pivnoy-laryok-07-bez-sdachi.png) | [PNG](cards/pivnoy-laryok-07-bez-sdachi.png) |
| 8 | На минутку | [PNG](buildings/pivnoy-laryok-08-minutka-source.png) | [PNG](buildings/pivnoy-laryok-08-minutka.png) | [PNG](cards/pivnoy-laryok-08-minutka.png) |
| 9 | Рыбный инспектор | [PNG](buildings/pivnoy-laryok-09-kot-source.png) | [PNG](buildings/pivnoy-laryok-09-kot.png) | [PNG](cards/pivnoy-laryok-09-kot.png) |
| 10 | Последний покупатель | [PNG](buildings/pivnoy-laryok-10-novyy-god-source.png) | [PNG](buildings/pivnoy-laryok-10-novyy-god.png) | [PNG](cards/pivnoy-laryok-10-novyy-god.png) |

Промпты и журнал генерации: `prompts/central-illustrations/pivnye-larki-generation-records.json`. Индивидуальные параметры: `prompts/central-illustrations/pivnoy-laryok-*.json`.

Повторная локальная обработка и сборка всех карт:
.venv/bin/python scripts/render_pivnye_larki.py

Параметры исходной карты сохранены: зелёная карта, активация 2–3, стоимость 1, «Возьмите 1 монету из банка. В свой ход».
