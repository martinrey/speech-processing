#!/usr/bin/env python

"""Google Cloud Speech API sample application using the REST API for batch
processing.

Example usage:
    python transcribe.py resources/audio.raw
    python transcribe.py gs://cloud-samples-tests/speech/brooklyn.flac
"""

import argparse
import io


def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    from google.cloud import speech
    speech_client = speech.Client()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()
        audio_sample = speech_client.sample(
            content=content,
            source_uri=None,
            encoding='LINEAR16',
            sample_rate_hertz=16000)

    alternatives = audio_sample.recognize('en-US')
    for alternative in alternatives:
        print('Transcript: {}'.format(alternative.transcript))


def transcribe_gcs(gcs_uri):
    """Transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    speech_client = speech.Client()

    audio_sample = speech_client.sample(
        content=None,
        source_uri=gcs_uri,
        encoding='FLAC',
        sample_rate_hertz=16000)

    alternatives = audio_sample.recognize('en-US')
    for alternative in alternatives:
        print('Transcript: {}'.format(alternative.transcript))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File or GCS path for audio file to be recognized')
    args = parser.parse_args()
    if args.path.startswith('gs://'):
        transcribe_gcs(args.path)
    else:
        transcribe_file(args.path)
