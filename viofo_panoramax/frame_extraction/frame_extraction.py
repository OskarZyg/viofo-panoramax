import datetime
import io
import os
import sys

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

def extract_image_sequence(video_in_path: str):
    # TODO: allow toggling of these options, especially deobf
    raw_gps_data = process_file(video_in_path, False, True)

    container = av.open(video_in_path)
    print(container.streams[0].metadata.get('creation_time'))

    probe = ffmpeg.probe(video_in_path)


    video_end_time = dateutil.parser.parse(probe['streams'][0]['tags']['creation_time']) # set/local tz!

    print(video_end_time)
    return

    video_end_time = video_end_time - datetime.timedelta(seconds=1) # account for some lag

    #video_frame_rate: int = eval(probe['streams'][0]['']) # danger! https://stackoverflow.com/a/9558001/15124094
    video_duration = datetime.timedelta(seconds=float(probe['streams'][0]['duration']))

    video_start_time = video_end_time - video_duration

    print(f"Video start time: {video_start_time}")

    raw_gps_data = [g for g in raw_gps_data if g is not None]


    last = None
    for gps in raw_gps_data:
        if gps:
            gps_dt = dateutil.parser.parse(gps['DT']['DT']) + datetime.timedelta(seconds=GPS_LAG_SECONDS)

            print(f"GPS Fix @ {gps_dt}")

            if last is not None and gps_dt - last < datetime.timedelta(seconds=1.5): # skip frames that will yield identically
                continue

            relative_video_time = gps_dt - video_start_time
            relative_video_time_seconds = relative_video_time.total_seconds()
            relative_video_time_base_units = int(relative_video_time_seconds / container.streams[0].time_base)

            print(f"Fix is {round(relative_video_time_seconds, 1)}s into video ({relative_video_time_base_units} base units)")

            last = gps_dt

            container.seek(relative_video_time_base_units, stream=container.streams[0])

            target_pts = relative_video_time_base_units
            f = None

            for frame in container.decode(video=0):
                if frame.pts is not None and frame.pts >= target_pts:
                    f = frame
                    break

            if f is None:
                continue  # ran out of frames — target was past end of decodable stream

            #frame.save(f'/Users/oskar/OneDrive/Git/viofo-panoramax/test_footage/frames/{gps['Loc']['Lat']['Float']},{gps['Loc']['Lon']['Float']}.jpg')
            img: Image = f.to_image()
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
                gps_ifd[ExifTags.GPS.GPSSpeed] = IFDRational(gps['Loc']['Speed'] / float(0.514444)) # we lose precision here! undoing fix_speed().

            if gps['Loc']['Bearing'] is not None:
                gps_ifd[ExifTags.GPS.GPSImgDirectionRef] = 'T'
                gps_ifd[ExifTags.GPS.GPSImgDirection] = IFDRational(gps['Loc']['Bearing'])

            img.save(f'/Users/oskar/OneDrive/Git/viofo-panoramax/test_footage/frames/{gps_dt.strftime('%Y-%m-%d %H:%M:%S')} {round(gps['Loc']['Lat']['Float'], 3)},{round(gps['Loc']['Lon']['Float'], 3)}.jpg', exif=exif)














if __name__ == '__main__':
    extract_image_sequence('/Users/oskar/Movies/Unreleased + Driving/20260519203638_203483F.MP4')