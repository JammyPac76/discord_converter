#!/usr/bin/python
from classes import *
from functions import compress_video, parse_arguments, download_video

def main():
    args = parse_arguments()

    if args.download == True:
        input_file = VideoFile(download_video(str(args.input_file)))
    else:
        input_file = VideoFile(str(args.input_file))

    output_file = VideoFile(str(args.output_file), imported_file=input_file)

    compress_video(input_file, output_file, target_size=args.size)

if __name__ == "__main__":
    main()
