# Программа с использованием OAuth Google и CalDav, перечисляющая последние события за неделю

## Установка пакетов:
```bash
poetry sync --no-root
```

## Подготовительные шаги:

- Необходимо прочитать документацию по работе с caldav в google calendar https://developers.google.com/workspace/calendar/caldav/v2/guide?hl=ru
- Активировать Google Calendar API https://console.cloud.google.com/apis/library/calendar-json.googleapis.com
- Выпустить креды (desktop app), сохранить в корень с именем credentials.json
- Добавить себя в тестировщики приложения через Google Auth Platform / Audience
- Запустить приложение, прожать auth, увидеть что все хорошо "The authentication flow has completed. You may close this window"
- Увидеть расписание за последнюю неделю


## Вывод приложения:
```
Event: Производственная практика (преддипломная), зачёт, Start: 2025-05-15 09:00:00+03:00
Event: Повторный зачет СХД / Менеджмент, Start: 2025-05-21 14:00:00+03:00
```