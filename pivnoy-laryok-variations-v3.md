# Пивные ларьки v3

Готовы все десять сцен в более мультяшной манере гаражей: чёткий тёмный контур, гладкая светотень и выразительные лица. Сюжеты, персонажи, предметы и постсоветский антураж сохранены.

Иллюстрации перерисованы встроенным image_gen отдельными запросами на белом фоне. Затем фон удалён локально. На сценах 05, 06, 08 и 10 мелкие псевдонадписи на упаковках локально заменены цветными полосками; исходники сохранены, обработка воспроизводится скриптом.

Для каждой сцены сохранены исходный PNG, PNG с прозрачностью, карточка, JSON промпта и shell-команда сборки. Предыдущие версии сохранены.

## Сцены

- А вот ту жвачку!: [карточка](cards/pivnoy-laryok-01-zhvachka-v3.png), [PNG с прозрачностью](buildings/pivnoy-laryok-01-zhvachka-v3.png), [исходник](buildings/pivnoy-laryok-01-zhvachka-v3-source.png), [промпт](prompts/central-illustrations/pivnoy-laryok-01-zhvachka-v3.json), [команда](card-commands/pivnoy-laryok-01-zhvachka-v3.sh).
- По одной — и домой: [карточка](cards/pivnoy-laryok-02-domoy-v3.png), [PNG с прозрачностью](buildings/pivnoy-laryok-02-domoy-v3.png), [исходник](buildings/pivnoy-laryok-02-domoy-v3-source.png), [промпт](prompts/central-illustrations/pivnoy-laryok-02-domoy-v3.json), [команда](card-commands/pivnoy-laryok-02-domoy-v3.sh).
- Под козырьком: [карточка](cards/pivnoy-laryok-03-kozyrek-v3.png), [PNG с прозрачностью](buildings/pivnoy-laryok-03-kozyrek-v3.png), [исходник](buildings/pivnoy-laryok-03-kozyrek-v3-source.png), [промпт](prompts/central-illustrations/pivnoy-laryok-03-kozyrek-v3.json), [команда](card-commands/pivnoy-laryok-03-kozyrek-v3.sh).
- Тропа народная: [карточка](cards/pivnoy-laryok-04-tropa-v3.png), [PNG с прозрачностью](buildings/pivnoy-laryok-04-tropa-v3.png), [исходник](buildings/pivnoy-laryok-04-tropa-v3-source.png), [промпт](prompts/central-illustrations/pivnoy-laryok-04-tropa-v3.json), [команда](card-commands/pivnoy-laryok-04-tropa-v3.sh).
- Большой футбол: [карточка](cards/pivnoy-laryok-05-futbol-v3.png), [PNG с прозрачностью](buildings/pivnoy-laryok-05-futbol-v3.png), [исходник](buildings/pivnoy-laryok-05-futbol-v3-source.png), [промпт](prompts/central-illustrations/pivnoy-laryok-05-futbol-v3.json), [команда](card-commands/pivnoy-laryok-05-futbol-v3.sh).
- Островок торговли: [карточка](cards/pivnoy-laryok-06-ostrovok-v3.png), [PNG с прозрачностью](buildings/pivnoy-laryok-06-ostrovok-v3.png), [исходник](buildings/pivnoy-laryok-06-ostrovok-v3-source.png), [промпт](prompts/central-illustrations/pivnoy-laryok-06-ostrovok-v3.json), [команда](card-commands/pivnoy-laryok-06-ostrovok-v3.sh).
- Без сдачи: [карточка](cards/pivnoy-laryok-07-bez-sdachi-v3.png), [PNG с прозрачностью](buildings/pivnoy-laryok-07-bez-sdachi-v3.png), [исходник](buildings/pivnoy-laryok-07-bez-sdachi-v3-source.png), [промпт](prompts/central-illustrations/pivnoy-laryok-07-bez-sdachi-v3.json), [команда](card-commands/pivnoy-laryok-07-bez-sdachi-v3.sh).
- На минутку: [карточка](cards/pivnoy-laryok-08-minutka-v3.png), [PNG с прозрачностью](buildings/pivnoy-laryok-08-minutka-v3.png), [исходник](buildings/pivnoy-laryok-08-minutka-v3-source.png), [промпт](prompts/central-illustrations/pivnoy-laryok-08-minutka-v3.json), [команда](card-commands/pivnoy-laryok-08-minutka-v3.sh).
- Рыбный инспектор: [карточка](cards/pivnoy-laryok-09-kot-v3.png), [PNG с прозрачностью](buildings/pivnoy-laryok-09-kot-v3.png), [исходник](buildings/pivnoy-laryok-09-kot-v3-source.png), [промпт](prompts/central-illustrations/pivnoy-laryok-09-kot-v3.json), [команда](card-commands/pivnoy-laryok-09-kot-v3.sh).
- Последний покупатель: [карточка](cards/pivnoy-laryok-10-novyy-god-v3.png), [PNG с прозрачностью](buildings/pivnoy-laryok-10-novyy-god-v3.png), [исходник](buildings/pivnoy-laryok-10-novyy-god-v3-source.png), [промпт](prompts/central-illustrations/pivnoy-laryok-10-novyy-god-v3.json), [команда](card-commands/pivnoy-laryok-10-novyy-god-v3.sh).

## Сборка

Из корня репозитория: `.venv/bin/python scripts/render_pivnye_larki_v3.py`. Скрипт использует сохранённые исходники, маски удаления фона и правки упаковок из `prompts/central-illustrations/pivnye-larki-v3-generation-records.json`.

Общий просмотр: `cards/pivnye-larki-v3-ten-art.jpg` и `cards/pivnye-larki-v3-ten-cards.jpg`.
