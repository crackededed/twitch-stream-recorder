import datetime
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
        self.root_path = "1"
        
        self.refresh = 10
        self.hls_segments = 1   # 1-10 for live stream, it's possible to use multiple threads to potentially increase the throughput. 2-3 is enough
    
    def run(self):
        # path to recorded stream
        self.recorded_path = os.path.join(self.root_path)
        if(os.path.isdir(self.recorded_path) is False):
            os.makedirs(self.recorded_path)
        
        # start
        logging.info("%s quality: %s", datetime.datetime.now().strftime("%m.%d %H:%M:%S"), self.quality)

        while True:
                # filename
                filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".ts"
                recorded_filename = os.path.join(self.recorded_path, filename)
                
                # start streamlink process
                subprocess.call(["streamlink", "--stream-segment-threads", str(self.hls_segments), "--hls-live-restart", "--twitch-disable-hosting", "--twitch-disable-ads", "--twitch-low-latency", "twitch.tv/" + self.username, self.quality, "--retry-streams", str(self.refresh)] + ["-o", recorded_filename])

                logging.info("%s disconnected", datetime.datetime.now().strftime("%m.%d %H:%M:%S"))
                time.sleep(1)

def main(argv):
    twitch_recorder = TwitchRecorder()
    logging.basicConfig(filename="twitch-recorder.log", encoding='utf-8', level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())
    twitch_recorder.run()

if __name__ == "__main__":
    main(sys.argv[1:])
