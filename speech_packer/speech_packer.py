import sys

import speech_recognition as sr

class SpeechAnalyzer(object):

    def __init__(self):
        # create recognizer and mic instances
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def process_single_phrase(self):
        phrase = SpeechAnalyzer.recognize_speech_from_mic(self.recognizer, self.microphone)
        if phrase["transcription"]:
            # show the user the transcription
            print("You said: {}".format(phrase["transcription"]))
            return phrase["transcription"]
        if not phrase["success"]:
            print("I didn't catch that. What did you say?\n")
            return None

        # if there was an error, stop
        assert(phrase["error"])
        raise Exception("ERROR: {}".format(phrase["error"]))

    @staticmethod
    def recognize_speech_from_mic(recognizer, microphone):
        """Transcribe speech from recorded from `microphone`.

        Returns a dictionary with three keys:
        "success": a boolean indicating whether or not the API request was
                   successful
        "error":   `None` if no error occured, otherwise a string containing
                   an error message if the API could not be reached or
                   speech was unrecognizable
        "transcription": `None` if speech could not be transcribed,
                   otherwise a string containing the transcribed text
        """
        # check that recognizer and microphone arguments are appropriate type
        if not isinstance(recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")

        # adjust the recognizer sensitivity to ambient noise and record audio
        # from the microphone
        print("Listening to microphone...")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, phrase_time_limit=5)

        # set up the response object
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        # try recognizing the speech in the recording
        # if a RequestError or UnknownValueError exception is caught,
        #     update the response object accordingly
        print("Analyzing...")
        try:
            response["transcription"] = recognizer.recognize_google(audio)
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"

        return response

class Packer(object):
    class Command(object):
        ADDITION = "addition"
        PACKING = "packing"
        DELETE = "delete"
        LIST = "list"
        STOP = "stop"

    def __init__(self, analyzer):
        self._speech_analyzer = analyzer
        self._to_pack = set()
        self._packed = set()
        self._commands = {self.Command.ADDITION, self.Command.PACKING, self.Command.DELETE, self.Command.LIST,
                          self.Command.STOP}

    def _get_item(self):
        print('What is the name of the item?')
        return self._speech_analyzer.process_single_phrase()

    def _add_item(self):
        text = self._get_item()
        self._to_pack.add(text)
        print("Item %s added" % text)

    def _pack_item(self):
        text = self._get_item()
        if text not in self._to_pack:
            print("Object needs to be added first")
            return
        self._to_pack.remove(text)
        self._packed.add(text)
        print("Item %s packed" % text)

    def _delete_item(self):
        text = self._get_item()
        if text in self._to_pack:
            self._to_pack.remove(text)
        if text in self._packed:
            self._packed.remove(text)
        print("Item %s is deleted" % text)

    def handle_command(self, command):
        if command == self.Command.ADDITION:
            self._add_item()
        elif command == self.Command.PACKING:
            self._pack_item()
        elif command == self.Command.DELETE:
            self._delete_item()
        elif command == self.Command.LIST:
            self.print_status()
        elif command == self.Command.STOP:
            self._stop()
        else:
            print("Unrecognized command")

    def _stop(self):
        self.print_status()
        sys.exit(0)

    def print_status(self):
        print("========================")
        print("Packing status:")
        print("Not packed:", self._to_pack)
        print("Packed:", self._packed)


if __name__ == "__main__":
    speech_analyzer = SpeechAnalyzer()
    packer = Packer(speech_analyzer)

    while True:
        print("========================")
        print('What do you want to do?\n'
          'Say "addition" to add to list,\n'
          'Say "packing" to indicate packing of item,\n'
          'Say "delete" to delete an item\n'
          'Say "list" to get list of items,\n'
          'Say "stop" to exit\n')

        try:
            text = speech_analyzer.process_single_phrase()
            packer.handle_command(text)
        except Exception as e:
            print(str(e))
            continue

    packer.print_status()