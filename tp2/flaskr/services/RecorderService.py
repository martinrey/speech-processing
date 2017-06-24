from flaskr.recorder.Recorder import Recorder


class RecorderService(object):
    def record(self):
        recorder = Recorder()
        recorder.record()
