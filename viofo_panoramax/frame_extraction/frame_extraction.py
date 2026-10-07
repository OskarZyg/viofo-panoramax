import datetime
import io
import os
import sys
from typing import Optional

from PIL import Image, ExifTags
import av
import dateutil
import ffmpeg
from PIL.TiffImagePlugin import IFDRational

from nvtk_mp42gpx import process_file, generate_gpx

GPS_LAG_SECONDS = -1.75

def deg_min_sec(value: float):
    """Convert a decimal degree float into EXIF's (deg, min, sec) rational triple."""
    value = abs(value)
    d = int(value)
    m_float = (value - d) * 60
    m = int(m_float)
    s = (m_float - m) * 60
    return (
        IFDRational(d, 1),
        IFDRational(m, 1),
        IFDRational(int(round(s * 100)), 100),
    )

def apply_exif(img: Image, gps_dt: datetime.datetime, gps: dict, rear: bool = False):
    exif: Image.Exif = img.getexif()

    gps_ifd = exif.get_ifd(ExifTags.IFD.GPSInfo)

    # https://www.chiark.greenend.org.uk/doc/libimage-exiftool-perl/html/TagNames/GPS.html
    gps_ifd[ExifTags.GPS.GPSLatitudeRef] = gps['Loc']['Lat']['Hemi']
    gps_ifd[ExifTags.GPS.GPSLatitude] = deg_min_sec(gps['Loc']['Lat']['Float'])

    gps_ifd[ExifTags.GPS.GPSLongitudeRef] = gps['Loc']['Lon']['Hemi']
    gps_ifd[ExifTags.GPS.GPSLongitude] = deg_min_sec(gps['Loc']['Lon']['Float'])

    gps_ifd[ExifTags.GPS.GPSTimeStamp] = (
        IFDRational(gps_dt.hour, 1),
        IFDRational(gps_dt.minute, 1),
        IFDRational(gps_dt.second, 1),
    )
    gps_ifd[ExifTags.GPS.GPSDateStamp] = gps_dt.strftime("%Y:%m:%d")

    if gps['Loc']['Speed'] is not None:
        gps_ifd[ExifTags.GPS.GPSSpeedRef] = 'N'
        gps_ifd[ExifTags.GPS.GPSSpeed] = IFDRational(
            gps['Loc']['Speed'] / float(0.514444))  # we lose precision here! undoing fix_speed().


    bearing = gps['Loc']['Bearing']
    if rear:
        bearing = (bearing + 180) % 360

    if gps['Loc']['Bearing'] is not None:
        gps_ifd[ExifTags.GPS.GPSImgDirectionRef] = 'T'
        gps_ifd[ExifTags.GPS.GPSImgDirection] = IFDRational(bearing)

    return exif

def extract_image_sequence(video_in_path: str, video_in_path_rear: Optional[str]):
    # TODO: allow toggling of these options, especially deobf
    raw_gps_data = process_file(video_in_path, False, True)

    container = av.open(video_in_path)
    camera_stream = container.streams[0]

    rear_camera_container = None
    rear_camera_stream = None
    if video_in_path_rear is not None:
        rear_camera_container = av.open(video_in_path_rear)
        rear_camera_stream = rear_camera_container.streams[0]

    creation_time_unsanitised = camera_stream.metadata.get('creation_time')
    duration_unsanitised = float(camera_stream.duration * camera_stream.time_base)

    assert creation_time_unsanitised is not None
    assert duration_unsanitised is not None

    video_end_time = dateutil.parser.parse(creation_time_unsanitised) # this tz-naive!
    video_end_time = video_end_time - datetime.timedelta(seconds=1) # account for some lag

    video_duration = datetime.timedelta(seconds=duration_unsanitised)

    video_start_time = video_end_time - video_duration

    print(f"Video start time: {video_start_time}")

    raw_gps_data = [g for g in raw_gps_data if g is not None]

    last = None
    for gps in raw_gps_data:
        if gps:
            gps_dt = dateutil.parser.parse(gps['DT']['DT']) + datetime.timedelta(seconds=GPS_LAG_SECONDS)

            # noinspection PyTypeChecker
            if last is not None and gps_dt - last < datetime.timedelta(seconds=1): # skip frames that will yield identically
                continue

            relative_video_time = gps_dt - video_start_time
            relative_video_time_seconds = relative_video_time.total_seconds()
            relative_video_time_base_units = int(relative_video_time_seconds / camera_stream.time_base)

            print(f"{gps_dt} fix is {round(relative_video_time_seconds, 1)}s into video ({relative_video_time_base_units} base units)")

            last = gps_dt

            container.seek(relative_video_time_base_units, stream=camera_stream)
            if rear_camera_container is not None:
                rear_camera_container.seek(relative_video_time_base_units, stream=rear_camera_stream)

            target_pts = relative_video_time_base_units
            f = None
            r = None

            for frame in container.decode(video=0):
                if frame.pts is not None and frame.pts >= target_pts:
                    f = frame
                    break

            if rear_camera_container is not None:
                for frame in rear_camera_container.decode(video=0):
                    if frame.pts is not None and frame.pts >= target_pts:
                        r = frame
                        break

                if r is None:
                    continue

            if f is None:
                continue  # ran out of frames — target was past end of decodable stream

            #frame.save(f'/Users/oskar/OneDrive/Git/viofo-panoramax/test_footage/frames/{gps['Loc']['Lat']['Float']},{gps['Loc']['Lon']['Float']}.jpg')
            img_f: Image = f.to_image()

            front_exif = apply_exif(img_f, gps_dt, gps)

            img_f.save(f'/Users/oskar/OneDrive/Git/viofo-panoramax/test_footage/frames/{gps_dt.strftime('%Y-%m-%d %H:%M:%S')} {round(gps['Loc']['Lat']['Float'], 3)},{round(gps['Loc']['Lon']['Float'], 3)}F.jpg', exif=front_exif)

            if r is not None:
                img_r: Image = r.to_image()
                rear_exif = apply_exif(img_r, gps_dt, gps)
                img_r.save(
                    f'/Users/oskar/OneDrive/Git/viofo-panoramax/test_footage/frames/{gps_dt.strftime('%Y-%m-%d %H:%M:%S')} {round(gps['Loc']['Lat']['Float'], 3)},{round(gps['Loc']['Lon']['Float'], 3)}R.jpg',
                    exif=rear_exif)


def extract_dir(path: str):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            if file.removesuffix('.MP4').endswith("F"):
                extract_image_sequence(file_path, None)












if __name__ == '__main__':
    PATH = '/Volumes/VOLUME1/DCIM/Movie'

    extract_dir(PATH)