import argparse, os, re, time, logging
from datetime import timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_offset(s):
    pattern = r'([+-]?\d+)d([+-]?\d+)h([+-]?\d+)m([+-]?\d+)s'
    m = re.match(pattern, s)
    if not m:
        raise ValueError(f"Invalid offset format: {s}")
    days = int(m.group(1))
    hours = int(m.group(2))
    minutes = int(m.group(3))
    seconds = int(m.group(4))
    total_seconds = days*86400 + hours*3600 + minutes*60 + seconds
    return timedelta(seconds=total_seconds)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input-directory', required=True)
    p.add_argument('--offset', required=True)
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args()

    offset = parse_offset(args.offset)
    logger.info(f"Using offset: {offset}")

    for name in os.listdir(args.input_directory):
        path = os.path.join(args.input_directory, name)
        if not os.path.isfile(path):
            continue
        st = os.stat(path)
        new_time = st.st_mtime + offset.total_seconds()
        if args.dry_run:
            logger.info(f"Would update {path} from {time.ctime(st.st_mtime)} to {time.ctime(new_time)}")
        else:
            logger.info(f"Updating {path} from {time.ctime(st.st_mtime)} to {time.ctime(new_time)}")
            os.utime(path, (new_time, new_time))

if __name__ == "__main__":
    main()
