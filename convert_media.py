"""
Конвертация аудиофайлов с помощью FFmpeg.

Лабораторная работа 1.1, вариант 1: WAV -> MP3.

Использование:
    python convert_media.py <входной_файл> <выходной_файл> [битрейт]

Примеры:
    python convert_media.py samples/sample.wav output/sample.mp3
    python convert_media.py samples/sample.wav output/sample.mp3 320k
"""

import os
import shutil
import subprocess
import sys

DEFAULT_BITRATE = '192k'


def check_ffmpeg():
    """
    Проверяет наличие FFmpeg в системе (в переменной PATH).

    :return: путь к исполняемому файлу ffmpeg
    :raises RuntimeError: FFmpeg не найден
    """
    ffmpeg_path = shutil.which('ffmpeg')

    if ffmpeg_path is None:
        raise RuntimeError(
            'FFmpeg не найден в PATH. Установите его с ffmpeg.org '
            'и добавьте папку bin в переменную среды PATH.'
        )

    return ffmpeg_path


def convert_file(input_path, output_path, bitrate=DEFAULT_BITRATE):
    """
    Конвертирует WAV в MP3 с помощью FFmpeg.

    :param input_path: путь к исходному файлу
    :param output_path: путь к выходному файлу
    :param bitrate: целевой битрейт аудио (например, '192k')
    :return: True при успехе
    :raises FileNotFoundError: исходный файл отсутствует
    :raises ValueError: неподходящие расширения файлов
    :raises RuntimeError: FFmpeg завершился с ошибкой
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f'Исходный файл не найден: {input_path}')

    input_extension = os.path.splitext(input_path)[1].lower()
    output_extension = os.path.splitext(output_path)[1].lower()

    if input_extension != '.wav':
        raise ValueError(
            f'Ожидался файл .wav, получен "{input_extension}"'
        )
    if output_extension != '.mp3':
        raise ValueError(
            f'Ожидался выходной файл .mp3, получен "{output_extension}"'
        )

    # Создаём выходную директорию, если её ещё нет.
    output_directory = os.path.dirname(os.path.abspath(output_path))
    os.makedirs(output_directory, exist_ok=True)

    # -hide_banner, -loglevel error - убираем лишний вывод FFmpeg
    # -y                            - перезаписывать выходной файл без вопросов
    # -codec:a libmp3lame           - кодек MP3
    # -b:a <битрейт>                - битрейт аудиопотока
    command = [
        'ffmpeg',
        '-hide_banner',
        '-loglevel', 'error',
        '-y',
        '-i', input_path,
        '-codec:a', 'libmp3lame',
        '-b:a', bitrate,
        output_path,
    ]

    print(f'Выполняется: {" ".join(command)}')
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(
            f'FFmpeg завершился с кодом {result.returncode}.\n'
            f'{result.stderr.strip()}'
        )

    return True


def main():
    """Точка входа: разбор аргументов, проверки, конвертация."""
    if len(sys.argv) < 3:
        print('Использование: python convert_media.py '
              '<входной_файл> <выходной_файл> [битрейт]')
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    bitrate = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_BITRATE

    try:
        ffmpeg_path = check_ffmpeg()
        print(f'FFmpeg найден: {ffmpeg_path}')

        convert_file(input_path, output_path, bitrate)
    except FileNotFoundError as error:
        print(f'Ошибка: {error}')
        sys.exit(1)
    except ValueError as error:
        print(f'Ошибка формата: {error}')
        sys.exit(1)
    except RuntimeError as error:
        print(f'Ошибка конвертации: {error}')
        sys.exit(1)

    size_kb = round(os.path.getsize(output_path) / 1024, 1)
    print(f'Конвертация завершена: {output_path} ({size_kb} КБ)')


if __name__ == '__main__':
    main()
