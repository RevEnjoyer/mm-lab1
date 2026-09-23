"""
Чтение метаданных аудиофайлов (MP3, WAV).

Лабораторная работа 1.1, вариант 1.
Читаемые метаданные: исполнитель, альбом, год (плюс длительность,
битрейт, частота дискретизации и число каналов).

Использование:
    python read_metadata.py <путь_к_файлу>
"""

import os
import sys

from mutagen import MutagenError
from mutagen.mp3 import MP3
from mutagen.wave import WAVE

# Поддерживаемые вариантом расширения
SUPPORTED_EXTENSIONS = ('.mp3', '.wav')

# Соответствие ID3-фреймов человекочитаемым названиям.
# TPE1 - исполнитель, TALB - альбом, TIT2 - название трека.
ID3_TEXT_FRAMES = (
    ('TIT2', 'Название'),
    ('TPE1', 'Исполнитель'),
    ('TALB', 'Альбом'),
)

# Год хранится по-разному в разных версиях ID3:
# ID3v2.4 - TDRC (полная дата), ID3v2.3 - TYER (только год).
ID3_YEAR_FRAMES = ('TDRC', 'TYER')


def extract_id3_tags(tags):
    """
    Извлекает текстовые ID3-теги (исполнитель, альбом, год, название).

    :param tags: объект тегов mutagen (ID3) или None, если тегов нет
    :return: словарь {название поля: значение}
    """
    result = {}

    # У файла может вообще не быть блока тегов - это не ошибка.
    if tags is None:
        return result

    for frame_id, title in ID3_TEXT_FRAMES:
        if frame_id in tags:
            # tags[frame_id].text - список значений, берём первое.
            value = str(tags[frame_id].text[0]).strip()
            if value:
                result[title] = value

    for frame_id in ID3_YEAR_FRAMES:
        if frame_id in tags:
            # TDRC может содержать '2019-05-01' - оставляем только год.
            value = str(tags[frame_id].text[0]).strip()
            if value:
                result['Год'] = value[:4]
            break

    return result


def read_audio_metadata(file_path):
    """
    Читает метаданные аудиофайла (MP3 или WAV).

    :param file_path: путь к файлу
    :return: словарь с метаданными
    :raises FileNotFoundError: файла не существует
    :raises ValueError: расширение не поддерживается вариантом
    :raises MutagenError: файл повреждён или не является аудиофайлом
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f'Файл не найден: {file_path}')

    extension = os.path.splitext(file_path)[1].lower()

    if extension == '.mp3':
        audio = MP3(file_path)
    elif extension == '.wav':
        audio = WAVE(file_path)
    else:
        raise ValueError(
            f'Неподдерживаемый формат "{extension}". '
            f'Вариант 1 работает с: {", ".join(SUPPORTED_EXTENSIONS)}'
        )

    info = audio.info
    metadata = {
        'Формат': extension.lstrip('.').upper(),
        'Размер файла, КБ': round(os.path.getsize(file_path) / 1024, 1),
        'Длительность, с': round(info.length, 2),
    }

    # bitrate в mutagen хранится в БИТАХ в секунду, поэтому делим на 1000.
    bitrate = getattr(info, 'bitrate', 0)
    if bitrate:
        metadata['Битрейт, кбит/с'] = round(bitrate / 1000)

    sample_rate = getattr(info, 'sample_rate', None)
    if sample_rate:
        metadata['Частота дискретизации, Гц'] = sample_rate

    channels = getattr(info, 'channels', None)
    if channels:
        metadata['Каналов'] = channels

    # Глубина в битах есть только у несжатого WAV.
    bits_per_sample = getattr(info, 'bits_per_sample', None)
    if bits_per_sample:
        metadata['Разрядность, бит'] = bits_per_sample

    # Теги (исполнитель, альбом, год) - основное требование варианта.
    tags = extract_id3_tags(audio.tags)
    if tags:
        metadata.update(tags)
    else:
        metadata['Теги'] = 'отсутствуют'

    return metadata


def print_metadata(file_path, metadata):
    """Аккуратно выводит словарь метаданных в консоль."""
    print(f'\nМетаданные для {file_path}:')
    print('-' * 48)

    # Выравниваем значения по самому длинному ключу.
    width = max(len(key) for key in metadata)
    for key, value in metadata.items():
        print(f'{key:<{width}} : {value}')
    print('-' * 48)


def main():
    """Точка входа: разбор аргументов, чтение, обработка ошибок."""
    if len(sys.argv) < 2:
        print('Использование: python read_metadata.py <файл>')
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        metadata = read_audio_metadata(file_path)
    except FileNotFoundError as error:
        print(f'Ошибка: {error}')
        sys.exit(1)
    except ValueError as error:
        print(f'Ошибка формата: {error}')
        sys.exit(1)
    except MutagenError as error:
        # Сюда попадают повреждённые файлы и файлы с "чужим" содержимым
        # (например, текстовый файл, переименованный в .mp3).
        print(f'Ошибка чтения метаданных (файл повреждён?): {error}')
        sys.exit(1)

    print_metadata(file_path, metadata)


if __name__ == '__main__':
    main()
