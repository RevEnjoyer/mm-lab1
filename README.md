# ЛР 1.1 — Настройка окружения и базовый ввод-вывод

Дисциплина: «Проектирование и программирование мультимедийных приложений».
**Вариант 1** (номер в журнале 20: `20 % 5 + 1 = 1`) — аудиофайлы.

| Параметр | Значение |
| --- | --- |
| Типы медиафайлов | MP3, WAV |
| Читаемые метаданные | исполнитель, альбом, год (+ длительность, битрейт, частота дискретизации) |
| Конвертация | WAV → MP3 |

## Состав проекта

| Файл | Назначение |
| --- | --- |
| `read_metadata.py` | чтение метаданных MP3/WAV через mutagen |
| `convert_media.py` | конвертация WAV → MP3 через FFmpeg |
| `requirements.txt` | зависимости Python |
| `.gitignore` | исключения для Git |
| `INSTRUCTIONS.md` | пошаговая инструкция по выполнению |

## Требования

- Python 3.8+
- mutagen 1.45+
- FFmpeg 6.x в PATH (ставится отдельно, не через pip)

## Установка

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Использование

```bash
python read_metadata.py samples\sample.wav
python convert_media.py samples\sample.wav output\sample.mp3
python convert_media.py samples\sample.wav output\hq.mp3 320k
```

## Обрабатываемые ошибки

- файл не найден;
- неподдерживаемое расширение;
- повреждённый медиафайл;
- FFmpeg отсутствует в PATH;
- ненулевой код возврата FFmpeg.
