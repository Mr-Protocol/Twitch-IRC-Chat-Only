'''
Modified from https://github.com/twitchdev/chatbot-python-sample/blob/main/chatbot.py

To get OAuth token: http://twitchapps.com/tmi/
'''

import sys
import irc.bot
import requests
import ssl

class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, token, channel):
        self.token = token
        self.channel = '#' + channel

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        # Original Port
        # port = 6667
        port = 6697
        print(f"Connecting to {server} on port {port} as {username}...\r\n")
        # Original connect command, plaintext connection
        # irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)
        factory = irc.connection.Factory(wrapper=ssl.wrap_socket)
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, "oauth:" + self.token)], username, username,connect_factory = factory)
        

    def on_welcome(self, c, e):
        print(f'Joining ' + self.channel)

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        print(e)

    def do_command(self, e, cmd):
        c = self.connection

def main():
    if len(sys.argv) != 4:
        print("Usage: twitchbot <username> <token> <channel>")
        print("Be sure to remove the oath: from the generated token.")
        sys.exit(1)

    username  = sys.argv[1]
    token     = sys.argv[2]
    channel   = sys.argv[3]

    bot = TwitchBot(username, token, channel)
    bot.start()

if __name__ == "__main__":
    main()
