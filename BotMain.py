#!/usr/bin/env python

import ConfigParser
import time
import subprocess
from slackclient import SlackClient


class SpotifyToSlackBot:
    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read('token.ini')
        self.slackApiToken = self.config.get('spotify', 'apitoken')

        self.slackClient = SlackClient(self.slackApiToken)
        self.botName = 'godify'
        self.botId = self.getBotId(self.botName)
        self.at_bot = "<@" + self.botId + ">"

        self.osaLines = { 'artist' : 'tell application "Spotify" to artist of current track as string',
                     'album' : 'tell application "Spotify" to album of current track as string',
                     'title' : 'tell application "Spotify" to name of current track as string'
                   }



        READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
        if self.slackClient.rtm_connect():
          print("StarterBot connected and running!")
          while True:
              command, channel = self.parse_slack_output(self.slackClient.rtm_read())

              if command and channel:
                print('Received message from: ' + str(channel) + ', containing: ' + str(command))
                self.handle_command(command, channel)
              time.sleep(READ_WEBSOCKET_DELAY)
        else:
                print("Connection failed. Invalid Slack token or bot ID?")

    def handle_command(self,command, channel):
        """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
        """
        response = "use /spotify or I won't do anything"
        if command.startswith('/spotify'):
            response = self.getSpotifyLinesOnMac()
        self.slackClient.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


    def getSpotifyLinesOnMac(self):
        #run osascripts
                proc = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        artist = proc.communicate(self.osaLines['artist'])[0][:-1]

        proc = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        album = proc.communicate(self.osaLines['album'])[0][:-1]

        proc = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        title = proc.communicate(self.osaLines['title'])[0][:-1]

        return 'Currently playing: ' + title + ', by: ' + artist + ', featured on album: ' + album


    def parse_slack_output(self,slack_rtm_output):
        """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
        """
        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                #print(output)
                if output and 'text' in output and self.at_bot in output['text']:
                    print('message for me!!!')
                    # return text after the @ mention, whitespace removed
                    return output['text'].split(self.at_bot)[1].strip().lower(), \
                       output['channel']
        return None, None

    def getBotId(self, name):
        apiCall = self.slackClient.api_call("users.list")
        if apiCall.get('ok'):
        # retrieve all users so we can find our bot
            users = apiCall.get('members')
            for user in users:
                if 'name' in user and user.get('name') == name:
                    return user.get('id')
        else:
            print("could not find bot user with the name " + BOT_NAME)



if __name__ == '__main__':
    bot = SpotifyToSlackBot()

