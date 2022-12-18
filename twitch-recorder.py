import datetime
import getopt
import logging
import os
import subprocess
import sys
import time


class TwitchRecorder:
    def __init__(self):
        # config
        self.username = ""
        self.quality = "best"
        self.root_path = ""
        
        self.refresh = "10"
        self.hls_segments = "1"   # 1-10 for live stream, it's possible to use multiple threads to potentially increase the throughput. 2-3 is enough
    
    def run(self):
        logging.info("%s quality: %s", datetime.datetime.now().strftime("%m.%d %H:%M:%S"), self.quality)

        while True:
                # start streamlink process
                subprocess.call([
                "streamlink", "twitch.tv/" + self.username, self.quality,
                "--twitch-disable-ads",
                "--twitch-low-latency",
                "--twitch-api-header", "X-Device-Id=twitch-web-wall-mason",
                "--twitch-access-token-param", "playerType=site",
                "--retry-streams", self.refresh,
                "--stream-segment-threads", self.hls_segments,
                "--hls-live-restart",
                "--output", os.path.join(self.root_path, "{author}", "{id}-{time:%Y%m%d_%H%M%S}.ts")
                ])

                logging.info("%s disconnected", datetime.datetime.now().strftime("%m.%d %H:%M:%S"))
                time.sleep(1)

def main(argv):
    twitch_recorder = TwitchRecorder()
    usage_message = "twitch-recorder.py -u <username> -q <quality>"
    logging.basicConfig(filename="twitch-recorder.log", encoding='utf-8', level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())

    try:
        opts, args = getopt.getopt(argv, "hu:q:", ["username=", "quality="])
    except getopt.GetoptError:
        print(usage_message)
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print(usage_message)
            sys.exit()
        elif opt in ("-u", "--username"):
            twitch_recorder.username = arg
        elif opt in ("-q", "--quality"):
            twitch_recorder.quality = arg

    twitch_recorder.run()


if __name__ == "__main__":
    main(sys.argv[1:])
