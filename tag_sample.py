"""
Вспомогательный скрипт: проставляет тестовые ID3-теги в аудиофайл
(MP3 или WAV).

Сгенерированный через FFmpeg тестовый sample.wav (синусоида) - это не
настоящая музыка, поэтому у него нет ни исполнителя, ни альбома: взять их
неоткуда. Скрипт имитирует то, что в реальности делает музыкальный
редактор/плеер - прописывает теги в файл один раз, ДО дальнейшей работы
с ним.

Рекомендуемый порядок:
    1. python tag_sample.py samples\\sample.wav      # теги в исходнике
    2. python read_metadata.py samples\\sample.wav   # видно теги в WAV
    3. python convert_media.py samples\\sample.wav output\\sample.mp3
    4. python read_metadata.py output\\sample.mp3    # теги перенеслись

Mutagen поддерживает ID3-теги как в MP3, так и в WAV (через встроенный
ID3-чанк), поэтому один и тот же код работает для обоих форматов.
FFmpeg при конвертации по умолчанию копирует метаданные, поэтому шаг 3
не требует никаких дополнительных флагов.

Использование:
    python tag_sample.py <файл.mp3|файл.wav> [исполнитель] [альбом] [год]
"""

import os
import sys

from mutagen.id3 import TALB, TDRC, TIT2, TPE1
from mutagen.mp3 import MP3
from mutagen.wave import WAVE

DEFAULT_TITLE = 'Test Tone'
DEFAULT_ARTIST = 'BSUIR'
DEFAULT_ALBUM = 'Multimedia Lab 1'
DEFAULT_YEAR = '2026'


def set_tags(file_path, artist=DEFAULT_ARTIST, album=DEFAULT_ALBUM,
             year=DEFAULT_YEAR, title=DEFAULT_TITLE):
    """Записывает ID3-теги в MP3- или WAV-файл (в обоих mutagen хранит их
    одинаково, поэтому дальше код общий)."""
    extension = os.path.splitext(file_path)[1].lower()

    if extension == '.mp3':
        audio = MP3(file_path)
    elif extension == '.wav':
        audio = WAVE(file_path)
    else:
        raise ValueError(f'Неподдерживаемый формат: {extension}')

    # Если у файла ещё нет блока ID3 - создаём его.
    if audio.tags is None:
        audio.add_tags()

    audio.tags.add(TIT2(encoding=3, text=title))
    audio.tags.add(TPE1(encoding=3, text=artist))
    audio.tags.add(TALB(encoding=3, text=album))
    audio.tags.add(TDRC(encoding=3, text=year))

    audio.save()


def main():
    if len(sys.argv) < 2:
        print('Использование: python tag_sample.py <файл.mp3|файл.wav> '
              '[исполнитель] [альбом] [год]')
        sys.exit(1)

    file_path = sys.argv[1]
    artist = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_ARTIST
    album = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_ALBUM
    year = sys.argv[4] if len(sys.argv) > 4 else DEFAULT_YEAR

    set_tags(file_path, artist=artist, album=album, year=year)
    print(f'Теги записаны в {file_path}: '
          f'исполнитель="{artist}", альбом="{album}", год="{year}"')


if __name__ == '__main__':
    main()
